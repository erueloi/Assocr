'''
Created on Mar 12, 2014

Copyright (c) 2014 Congressus, The Netherlands

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.

@author: Congressus
@license: MIT License
@version: 1.0
'''

import xml.etree.cElementTree as ET
import pprint
import random
import sys
import hashlib
import time
import datetime
from xml.sax.saxutils import escape


class PySepaDD(object):
    '''
    This class creates a Sepa Direct Debit XML File.
    '''

    def __init__(self, config):
        '''
        Constructor. Checks the config, prepares the document and
        builds the header.
        @param param: The config dict.
        @raise exception: When the config dict is invalid.
        '''
        self._config = None             # Will contain the config file.
        self._xml = None                # Will contain the final XML file.
        self._batches = dict()          # Will contain the SEPA batches.
        self._batch_totals = dict()     # Will contain the total amount to
                                        # debit per batch for checksum total.

        config_result = self.check_config(config)
        self._config = config

        self._prepare_document()
        self._create_header()

    def check_config(self, config):
        '''
        Check the config file for required fields and validity.

        @param config: The config dict.
        @raise exception: if the config dict is invalid
        '''
        validation = ""
        required = ["name", "IBAN", "BIC", "creditor_id", "currency"]

        for config_item in required:
            if not config_item in config:
                validation += config_item.upper() + "_MISSING "

        if validation:
            raise Exception("Config file did not validate. " + validation)


    def check_payment(self, payment):
        '''
        Check the config file for required fields and validity.
        @param payment: The payment dict
        @raise exception: if payment is invalid
        '''

        validation = ""
        required= ['IBAN', 'BIC', 'amount', 'type', 'collection_date', 'mandate_id', 'mandate_date', 'description']

        for payment_item in required:
            if not payment_item in payment:
                validation += payment_item.upper() + "_MISSING "

        if 'amount' in payment:
            if not isinstance(payment['amount'], int):
                validation += 'AMOUNT_NOT_INTEGER'
            elif payment['amount'] < 0:
                validation += 'AMOUNT_NEGATIVE'

        if 'mandate_date' in  payment and not isinstance(payment['mandate_date'], datetime.date):
            validation += "MANDATE_DATE_INVALID_OR_NOT_DATETIME_INSTANCE"
            payment['mandate_date'] = str(payment['mandate_date'])
        else:
            payment['mandate_date'] = payment['mandate_date'].strftime('%Y-%m-%d')

        if 'collection_date' in payment and not isinstance(payment['collection_date'], datetime.date):
            validation += "COLLECTION_DATE_INVALID_OR_NOT_DATETIME_INSTANCE"
            payment['collection_date'] = str(payment['collection_date'])
        else:
            payment['collection_date'] = payment['collection_date'].strftime('%Y-%m-%d')


        if validation:
            raise Exception('Payment did not validate: ' + validation + '\n' + 'payment content was:\n' + pprint.pformat(payment))



    def add_payment(self, payment):
        '''
        Function to add payments
        @param payment: The payment dict
        @raise: exception if the payment is invalid
        '''
        self.check_payment(payment)

        TX_nodes = self._create_TX_node()
        TX_nodes['InstdAmtNode'].set("Ccy", self._config['currency'])
        TX_nodes['InstdAmtNode'].text = self.int_to_decimal_str(
                                        payment['amount'])

        TX_nodes['MndtIdNode'].text = payment['mandate_id']
        TX_nodes['DtOfSgntrNode'].text = payment['mandate_date']
        TX_nodes['BIC_DbtrAgt_Node'].text = payment['BIC']

        TX_nodes['Nm_Dbtr_Node'].text = escape(payment['name'])
        TX_nodes['IBAN_DbtrAcct_Node'].text = payment['IBAN']
        TX_nodes['UstrdNode'].text = escape(payment['description'])
        TX_nodes['EndToEndIdNode'].text = self._make_id()

        self._add_batch(TX_nodes, payment)



    def export(self):
        '''
        Method to output the xml as string. It will finalize the batches and
        then calculate the checksums (amount sum and transaction count),
        fill these into the group header and output the XML.
        '''
        self._finalize_batch()

        ctrl_sum_total = 0
        nb_of_txs_total = 0

        for ctrl_sum in self._xml.iter('CtrlSum'):
            if ctrl_sum.text is None:
                continue
            ctrl_sum_total += self.decimal_str_to_int(ctrl_sum.text)

        for nb_of_txs in self._xml.iter('NbOfTxs'):
            if nb_of_txs.text is None:
                continue
            nb_of_txs_total += int(nb_of_txs.text)

        CstmrDrctDbtInitn_node = self._xml.find('CstmrDrctDbtInitn')
        GrpHdr_node = CstmrDrctDbtInitn_node.find('GrpHdr')
        CtrlSum_node = GrpHdr_node.find('CtrlSum')
        NbOfTxs_node = GrpHdr_node.find('NbOfTxs')
        CtrlSum_node.text = self.int_to_decimal_str(ctrl_sum_total)
        NbOfTxs_node.text = str(nb_of_txs_total)

        #Prepending the XML version is hacky, but cElementTree only offers this
        #automatically if you write to a file, which we don't necessarily want.
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + ET.tostring(
               self._xml, "utf-8")

    def _prepare_document(self):
        '''
        Build the main document node and set xml namespaces.
        '''
        self._xml = ET.Element("Document")
        self._xml.set("xmlns",
                      "urn:iso:std:iso:20022:tech:xsd:pain.008.003.02")
        self._xml.set("xmlns:xsi",
                      "http://www.w3.org/2001/XMLSchema-intance")
        ET.register_namespace("",
                              "urn:iso:std:iso:20022:tech:xsd:pain.008.003.02")
        ET.register_namespace("xsi",
                              "http://www.w3.org/2001/XMLSchema-intance")
        CstmrDrctDbtInitn_node = ET.Element("CstmrDrctDbtInitn")
        self._xml.append(CstmrDrctDbtInitn_node)

    def _create_header(self):
        '''
        Function to create the GroupHeader (GrpHdr) in the
        CstmrDrctDbtInit Node
        '''
        # Retrieve the node to which we will append the group header.
        CstmrDrctDbtInitn_node = self._xml.find('CstmrDrctDbtInitn')

        # Create the header nodes.
        GrpHdr_node = ET.Element("GrpHdr")
        MsgId_node = ET.Element("MsgId")
        CreDtTm_node = ET.Element("CreDtTm")
        NbOfTxs_node = ET.Element("NbOfTxs")
        CtrlSum_node = ET.Element("CtrlSum")
        InitgPty_node = ET.Element("InitgPty")
        Nm_node = ET.Element("Nm")

        # Add data to some header nodes.
        MsgId_node.text = self._make_msg_id()
        CreDtTm_node.text = datetime.datetime.now()\
                            .strftime('%Y-%m-%dT%H:%M:%S')
        Nm_node.text = self._config['name']

        # Append the nodes
        InitgPty_node.append(Nm_node)
        GrpHdr_node.append(MsgId_node)
        GrpHdr_node.append(CreDtTm_node)
        GrpHdr_node.append(NbOfTxs_node)
        GrpHdr_node.append(CtrlSum_node)
        GrpHdr_node.append(InitgPty_node)

        # Append the header to its parent
        CstmrDrctDbtInitn_node.append(GrpHdr_node)

    def _create_PmtInf_node(self):
        '''
        Method to create the blank payment information nodes as a dict.
        '''
        ED = dict()  # ED is element dict
        ED['PmtInfNode'] = ET.Element("PmtInf")
        ED['PmtInfIdNode'] = ET.Element("PmtInfId")
        ED['PmtMtdNode'] = ET.Element("PmtMtd")
        ED['BtchBookgNode'] = ET.Element("BtchBookg")
        ED['NbOfTxsNode'] = ET.Element("NbOfTxs")
        ED['CtrlSumNode'] = ET.Element("CtrlSum")
        ED['PmtTpInfNode'] = ET.Element("PmtTpInf")
        ED['SvcLvlNode'] = ET.Element("SvcLvl")
        ED['Cd_SvcLvl_Node'] = ET.Element("Cd")
        ED['LclInstrmNode'] = ET.Element("LclInstrm")
        ED['Cd_LclInstrm_Node'] = ET.Element("Cd")
        ED['SeqTpNode'] = ET.Element("SeqTp")
        ED['ReqdColltnDtNode'] = ET.Element("ReqdColltnDt")
        ED['CdtrNode'] = ET.Element("Cdtr")
        ED['Nm_Cdtr_Node'] = ET.Element("Nm")
        ED['CdtrAcctNode'] = ET.Element("CdtrAcct")
        ED['Id_CdtrAcct_Node'] = ET.Element("Id")
        ED['IBAN_CdtrAcct_Node'] = ET.Element("IBAN")
        ED['CdtrAgtNode'] = ET.Element("CdtrAgt")
        ED['FinInstnId_CdtrAgt_Node'] = ET.Element("FinInstnId")
        ED['BIC_CdtrAgt_Node'] = ET.Element("BIC")
        ED['ChrgBrNode'] = ET.Element("ChrgBr")
        ED['CdtrSchmeIdNode'] = ET.Element("CdtrSchmeId")
        ED['Id_CdtrSchmeId_Node'] = ET.Element("Id")
        ED['PrvtIdNode'] = ET.Element("PrvtId")
        ED['OthrNode'] = ET.Element("Othr")
        ED['Id_Othr_Node'] = ET.Element("Id")
        ED['SchmeNmNode'] = ET.Element("SchmeNm")
        ED['PrtryNode'] = ET.Element("Prtry")
        return ED

    def _create_TX_node(self):
        '''
        Method to create the blank transaction nodes as a dict.
        '''
        ED = dict()
        ED['DrctDbtTxInfNode'] = ET.Element("DrctDbtTxInf")
        ED['PmtIdNode'] = ET.Element("PmtId")
        ED['EndToEndIdNode'] = ET.Element("EndToEndId")
        ED['InstdAmtNode'] = ET.Element("InstdAmt")
        ED['DrctDbtTxNode'] = ET.Element("DrctDbtTx")
        ED['MndtRltdInfNode'] = ET.Element("MndtRltdInf")
        ED['MndtIdNode'] = ET.Element("MndtId")
        ED['DtOfSgntrNode'] = ET.Element("DtOfSgntr")
        ED['DbtrAgtNode'] = ET.Element("DbtrAgt")
        ED['FinInstnId_DbtrAgt_Node'] = ET.Element("FinInstnId")
        ED['BIC_DbtrAgt_Node'] = ET.Element("BIC")
        ED['DbtrNode'] = ET.Element("Dbtr")
        ED['Nm_Dbtr_Node'] = ET.Element("Nm")
        ED['DbtrAcctNode'] = ET.Element("DbtrAcct")
        ED['Id_DbtrAcct_Node'] = ET.Element("Id")
        ED['IBAN_DbtrAcct_Node'] = ET.Element("IBAN")
        ED['RmtInfNode'] = ET.Element("RmtInf")
        ED['UstrdNode'] = ET.Element("Ustrd")
        return ED


    def _add_batch(self, TX_nodes, payment):
        '''
        Method to add a payment as a batch. The transaction details are already
        present. Will fold the nodes accordingly and the call the
        _add_to_batch_list function to store the batch.
        '''
        TX_nodes['PmtIdNode'].append(TX_nodes['EndToEndIdNode'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['PmtIdNode'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['InstdAmtNode'])

        TX_nodes['MndtRltdInfNode'].append(TX_nodes['MndtIdNode'])
        TX_nodes['MndtRltdInfNode'].append(TX_nodes['DtOfSgntrNode'])
        TX_nodes['DrctDbtTxNode'].append(TX_nodes['MndtRltdInfNode'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['DrctDbtTxNode'])

        TX_nodes['FinInstnId_DbtrAgt_Node'].append(
                                            TX_nodes['BIC_DbtrAgt_Node'])
        TX_nodes['DbtrAgtNode'].append(TX_nodes['FinInstnId_DbtrAgt_Node'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['DbtrAgtNode'])

        TX_nodes['DbtrNode'].append(TX_nodes['Nm_Dbtr_Node'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['DbtrNode'])

        TX_nodes['Id_DbtrAcct_Node'].append(TX_nodes['IBAN_DbtrAcct_Node'])
        TX_nodes['DbtrAcctNode'].append(TX_nodes['Id_DbtrAcct_Node'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['DbtrAcctNode'])

        TX_nodes['RmtInfNode'].append(TX_nodes['UstrdNode'])
        TX_nodes['DrctDbtTxInfNode'].append(TX_nodes['RmtInfNode'])
        self._add_to_batch_list(TX_nodes, payment)

    def _add_to_batch_list(self, TX, payment):
        '''
        Method to add a transaction to the batch list. The correct batch will
        be determined by the payment dict and the batch will be created if
        not existant. This will also add the payment amount to the respective
        batch total.
        '''
        batch_key = payment['type'] + "::" + payment['collection_date']

        if not batch_key in self._batches.keys():
            self._batches[batch_key] = []
            self._batch_totals[batch_key] = 0

        self._batches[batch_key].append(TX['DrctDbtTxInfNode'])

        if batch_key in self._batch_totals:
            self._batch_totals[batch_key] += payment['amount']



    def _finalize_batch(self):
        '''
        Method to finalize the batch, this will iterate over the _batches dict
        and create a PmtInf node for each batch. The correct information (from
        the batch_key and batch_totals) will be inserted and the batch
        transaction nodes will be folded. Finally, the batches will be added to
        the main XML.
        '''
        for batch_meta, batch_nodes in self._batches.items():
            batch_meta_split = batch_meta.split("::")
            PmtInf_nodes = self._create_PmtInf_node()
            PmtInf_nodes['PmtInfIdNode'].text = self._make_id()
            PmtInf_nodes['PmtMtdNode'].text = "DD"
            PmtInf_nodes['BtchBookgNode'].text = "true"
            PmtInf_nodes['Cd_SvcLvl_Node'].text = "SEPA"
            PmtInf_nodes['Cd_LclInstrm_Node'].text = "CORE"
            PmtInf_nodes['SeqTpNode'].text = batch_meta_split[0]
            PmtInf_nodes['ReqdColltnDtNode'].text = batch_meta_split[1]
            PmtInf_nodes['Nm_Cdtr_Node'].text = escape(self._config['name'])
            PmtInf_nodes['IBAN_CdtrAcct_Node'].text = self._config['IBAN']

            PmtInf_nodes['BIC_CdtrAgt_Node'].text = self._config['BIC']

            PmtInf_nodes['ChrgBrNode'].text = "SLEV"
            PmtInf_nodes['Id_Othr_Node'].text = self._config['creditor_id']
            PmtInf_nodes['PrtryNode'].text = "SEPA"

            PmtInf_nodes['NbOfTxsNode'].text = str(len(batch_nodes))
            PmtInf_nodes['CtrlSumNode'].text = self.int_to_decimal_str(
                                               self._batch_totals[batch_meta])

            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['PmtInfIdNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['PmtMtdNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['BtchBookgNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['NbOfTxsNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['CtrlSumNode'])

            PmtInf_nodes['SvcLvlNode'].append(PmtInf_nodes['Cd_SvcLvl_Node'])
            PmtInf_nodes['LclInstrmNode'].append(
                                          PmtInf_nodes['Cd_LclInstrm_Node'])
            PmtInf_nodes['PmtTpInfNode'].append(PmtInf_nodes['SvcLvlNode'])
            PmtInf_nodes['PmtTpInfNode'].append(PmtInf_nodes['LclInstrmNode'])
            PmtInf_nodes['PmtTpInfNode'].append(PmtInf_nodes['SeqTpNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['PmtTpInfNode'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['ReqdColltnDtNode'])

            PmtInf_nodes['CdtrNode'].append(PmtInf_nodes['Nm_Cdtr_Node'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['CdtrNode'])

            PmtInf_nodes['Id_CdtrAcct_Node'].append(
                                            PmtInf_nodes['IBAN_CdtrAcct_Node'])
            PmtInf_nodes['CdtrAcctNode'].append(
                                         PmtInf_nodes['Id_CdtrAcct_Node'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['CdtrAcctNode'])

            PmtInf_nodes['FinInstnId_CdtrAgt_Node'].append(
                                        PmtInf_nodes['BIC_CdtrAgt_Node'])
            PmtInf_nodes['CdtrAgtNode'].append(
                                       PmtInf_nodes['FinInstnId_CdtrAgt_Node'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['CdtrAgtNode'])

            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['ChrgBrNode'])

            PmtInf_nodes['OthrNode'].append(PmtInf_nodes['Id_Othr_Node'])
            PmtInf_nodes['SchmeNmNode'].append(PmtInf_nodes['PrtryNode'])
            PmtInf_nodes['OthrNode'].append(PmtInf_nodes['SchmeNmNode'])
            PmtInf_nodes['PrvtIdNode'].append(PmtInf_nodes['OthrNode'])
            PmtInf_nodes['Id_CdtrSchmeId_Node'].append(
                                                PmtInf_nodes['PrvtIdNode'])
            PmtInf_nodes['CdtrSchmeIdNode'].append(
                                           PmtInf_nodes['Id_CdtrSchmeId_Node'])
            PmtInf_nodes['PmtInfNode'].append(PmtInf_nodes['CdtrSchmeIdNode'])

            for txnode in batch_nodes:
                PmtInf_nodes['PmtInfNode'].append(txnode)

            CstmrDrctDbtInitn_node = self._xml.find('CstmrDrctDbtInitn')
            CstmrDrctDbtInitn_node.append(PmtInf_nodes['PmtInfNode'])

    def _get_rand_string(self, size):
        '''
        Create a random hex string of certain size, to be used for ids.
        @param size: integer definining length of random string (max 40).
        @return: a random hex string of length size, will never return more
        than 40 chars.
        '''
        random_number = random.randint(0, sys.maxint)   # Weak random, but it
                                                        # is not used for any
                                                        # crypto
        random_string = hashlib.sha1(str(random_number)).hexdigest()
        return random_string[:size]

    def _make_msg_id(self):
        '''
        Create a semi random message id, by using 12 char random hex string and
        a timestamp.
        @return: string consisting of timestamp, -, random value
        '''
        random_string = self._get_rand_string(12)
        timestamp = time.strftime("%d%m%Y%I%M%S")
        msg_id = timestamp + "-" + random_string
        return msg_id

    def _make_id(self):
        '''
        Create a random id combined with the creditor name.
        @return string consisting of name (truncated at 22 chars), -,
        12 char rand hex string.
        '''
        random = self._get_rand_string(12)
        name = self._config['name']
        if len(name) > 22:
            name = name[:22]
        return name + "-" + random

    def int_to_decimal_str(self, integer):
        '''
        Helper to convert integers (representing cents) into decimal currency
        string. WARNING: DO NOT TRY TO DO THIS BY DIVISION, FLOATING POINT
        ERRORS ARE NO FUN IN FINANCIAL SYSTEMS.
        @param integer The amount in cents
        @return string The amount in currency with full stop decimal separator
        '''
        int_string = str(integer)
        if len(int_string) < 2:
            return "0." + int_string.zfill(2)
        else:
            return int_string[:-2] + "." + int_string[-2:]

    def decimal_str_to_int(self, decimal_string):
        '''
        Helper to decimal currency string into integers (cents).
        WARNING: DO NOT TRY TO DO THIS BY CONVERSION AND MULTIPLICATION,
        FLOATING POINT ERRORS ARE NO FUN IN FINANCIAL SYSTEMS.
        @param string The amount in currency with full stop decimal separator
        @return integer The amount in cents
        '''
        int_string = decimal_string.replace('.', '')
        int_string = int_string.lstrip('0')
        return int(int_string)
