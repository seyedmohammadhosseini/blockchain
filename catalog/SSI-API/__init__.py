import asyncio, json, pprint
from indy import pool, ledger, wallet, did, anoncreds, crypto
from indy.error import IndyError
import random
from catalog.Sovrin.assets import config
from catalog.Sovrin.library import message
import subprocess
import requests

class controller:

    def __init__(self, action, libraries):

        self.master_secret_id = "Master Secret"
        self.server = "http://192.168.94.161:14265"
        self.headers = {'Content-type': 'application/json'}

        self.cred_offer = ""
        self._cred_def_ = ""
        self.myCredit = ""
        self.wallet_handle = None

        self.prover = {
            'did': 'VsKV7grR1BUE29mG2Fm2kX',
            'wallet_config': json.dumps({"id": "prover_wallet"}),
            'wallet_credentials': json.dumps({"key": "issuer_wallet_key"})
        }

        loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.get_credential())
        loop.run_until_complete(self.get_token())
        loop.close()

    async  def get_token(self):
        try:
            print("1- The client should have an Indy wallet")
            #await wallet.create_wallet(self.prover['wallet_config'], self.prover['wallet_credentials'])

            print('2- Then the wallet should be opened')
            self.wallet_handle = await wallet.open_wallet(self.prover['wallet_config'], self.prover['wallet_credentials'])

            print("3- to ensure a secure connection between the handler and the client, pairwise DIDs are created.")
            print('   The client now creates a DID, verkey (public key) and a private key and stores them in the wallet')
            did_json = json.dumps({})
            _did_, _verkey_ = await did.create_and_store_my_did(self.wallet_handle, did_json)

            json_request = {"did": _did_, "verkey": _verkey_}

            response_one = requests.post(self.server + "/did", json=json_request, headers=self.headers)

            if response_one.status_code == 200:

                print("4- To decode the message, the previous response must be unpacked.")
                unpack_json = await crypto.unpack_message(self.wallet_handle, response_one.content)
                unpack_json = unpack_json.decode('utf-8')
                unpack_json = json.loads(unpack_json)['message']
                unpack_json = json.loads(unpack_json)

                schemas = '{"100":{"ver": "1.0", "id": "69aWwGn8QxWG2HjYb8E4SY:2:thing:1.0", "name": "thing", "version": "1.0", "attrNames": ["pow_capable", "priority", "id", "type"], "seqNo": 100}}'
                credential_definitions = '{"69aWwGn8QxWG2HjYb8E4SY:3:CL:100:thing_cdef":{"ver":"1.0","id":"69aWwGn8QxWG2HjYb8E4SY:3:CL:100:thing_cdef","schemaId":"100","type":"CL","tag":"thing_cdef","value":{"primary":{"n":"101546675695904491693632217887159716244840350713357258354897040773854069176572277472146943511953263072998090688628905044249421788737203637464406352950696829270948579971196789553114032745715802394436970860294535320386331526721227431181305087661652360417464727986223410885579468036359464706557921594554520010653972849229756180399046427127370177580336689133426436051813943014507564052105039210739968060213422106413987973871965127057427169781385367481348937847290214337427534943649230093469063934971293141272701129368483838410549944373705422857990662456977084056260799857357415592460800708722463690124641011243834985473401","s":"78949397174819746720209684446771029872992362219438315820905337270174949085617729258140555693823796496689369219545010683137413200331079236990695586476492746527970594115342240857083699863098757934920629487056402731621279725161316731266027144720374117217937206990159276377014224638023508935051767620012148109964772215708648055887549083850863896196422339390379699806281444631347414358771471505967070937337512355112960398611297945254553935921787572737936658918414648875015267278406067040145126760911497816956095656641521302455888587509999942636204309844485606879105254585229649065054717148864687951679200757681426262133506","r":{"master_secret":"8722673013562307861662122353824328893844154470560526641422967678336212996657245449724458813643383607793847933774023454059913117752039604540334784908562177455107936668059870782264587897888638381265104040438919275616240023005198903948546805061215637821143996747457028801367229085596106003243613159991012911970361396555953013148369293350318682514714747331322690183494318291088639635086478328584638350687689286668898460052877613229966835152156564761594162284449948439746463939532567469433709053424786354861829534394339303812131032496340846530195018726545230326374410406309110984193399887082276343299496286237338610125653","id":"59749584030119517592925482149796812929217892787850637274076241559581413297149208090626626674924412509208556154393048592612091278327209849185517933832734453563723866739579259363090605559649514580669491775050859437473486544018346700528495951645053073954407297624280548471502941130916633616521865281837467536757074350234998398896019993386448556857085344623307330061121061055157868382922876095500037434767724354734075243559341475956188221169357277740762464083438464878085864219611032769314514273459765540660254074380079952554540205737086087816685857592826653810061222768791468751876407192682800686811989408271687617324462","type":"95583416390303156689478702916140981068258360511275105954710167128460621554289583301482624988183223540847377803940941861221869064698689483958636204930480536229458862056945433130814954247378473202795149877963339513595692900310409466743124571795360077973720350064513130178379564732710483452541271528331316898910676046376134650441554939294016214558944066734648794536970803161137421497894689189793034067282198173548337433279142575790027626639357052566790016845342529319142843048027929732188791650827079822807993207976625517605915758989030298814496527457232797216817392042791884582395925490109588775286134746324181922728159","pow_capable":"19431174634531684541811145690739611124221861751305001650465322784551135242098491064440215016581814818056155417371921507012781049716171090383502948204507304543671664861474455108831263419128969460675095971504346007312118430497057474735184187830546558924295933123246474895672445449563615557778040610818089032167431094801917936555717501623035733234628231187095892544046551363182099646588642765731700972340752250133097623435627834921327765129412614683963559726695864660766172242048290887275675093841056326720286120416572267093641528881021481066772880271525998838385690192312671752468671634979164912493496721976403977341769","priority":"47026188416972682229824882327095824635002647528730816268930655112254529230991521820160924124436933584661230807547910975240677000394833105530737456437007322124390303564720162919034937805923714015271520359818902591440562987868803200909059255211953474620255287262273370861894588823434797949818490117881330325727268011879054954647753822294042600714914522579179452489924028123441162017076845967814604522055965135925773723121504492441844126553626061909182224860385889008471746947201598546700391131092227497662397657437846269059680832187262380305712402461619909493181415938948204635783174145093145923314800229575752056837212"},"rctxt":"98051826194871911144952195676509852282612385777179868584884385891867983780877804666238433080158337992989511280280760463993474231641060497140417931174582002777421855791130225642477592454047896627010251517857129047316618509098706339864756887556723187845982669105960479295622258510155457871023687054093872732825584668015732281264776233564468800506611623810478606940204456764736939352481038835220246026533592322478877815904752887941640239889567916469161752932447155368390194907133855339866088802893654198896470263490635898592927317833010728474921544379305873108064454732716367192072064141865152063598802334501457235857439","z":"28842976133981076049305020366938287863027503699524253737179113060609916625318827506598965173198824779264702032256714464209450072850621512186713697658374574149058340491672139088151501298201358952512212639092309624878798493412957341894401235973759308863632246986832008344876591637927585050861077636545194003966384759982700969658202997535423227272924507976417327878662094893226625719446185702932902883128144632484737851285557401248447217616340929869280452713655084853432365257479333042321007467666089764463473320856629321260820243532788426513663517077407812770387830266978089336823237643546526605430503552528603898793201"}}}}'
                cardentials_for_create_proof = '{"self_attested_attributes": {}, "requested_attributes": {"attr1_referent": {"cred_id": "69aWwGn8QxWG2HjYb8E4SY:3:CL:100:thing_cdef", "revealed": true}}, "requested_predicates": {}}'

                revoc_regs_json = json.dumps({})

                proof = await anoncreds.prover_create_proof(
                    self.wallet_handle,
                    json.dumps(unpack_json['proof_request']),
                    cardentials_for_create_proof,
                    self.master_secret_id,
                    schemas,
                    credential_definitions,
                    revoc_regs_json
                )

                jwe_object = crypto.pack_message(
                    self.wallet_handle,
                    json.dumps(proof).encode(),
                    str(unpack_json['verkey']),
                    _verkey_
                )

                json_request_two = {"jwe": str(jwe_object)}
                response_two = requests.post(self.server + "/token", json=json_request_two, headers=self.headers)
                if response_one.status_code == 200:
                    print("5- The handler now analyzes the received JWE.")
                    unpack_two = await crypto.unpack_message(self.wallet_handle, response_two.content)
                    unpack_two = unpack_two.decode('utf-8')
                    unpack_two = json.loads(unpack_two)['message']
                    unpack_two = json.loads(unpack_two)
                    exit(unpack_two)

                    attach_commend = {
                        "command" : "attachToTangle",
                        "trunkTransaction" : "",
                        "branchTransaction" : "",
                        "minWeightMagnitude" : 14,
                        "trytes" : "",
                        "priority" : "",
                        "accessToken" : ""
                    }

                    jwe_object = crypto.pack_message(
                        self.wallet_handle,
                        json.dumps(attach_commend).encode(),
                        str(unpack_json['verkey']),
                        _verkey_
                    )
                    json_request_three = {"jwe": str(jwe_object)}
                    response_three = requests.post(self.server, json=json_request_three, headers=self.headers)

                    unpack_three = await crypto.unpack_message(self.wallet_handle, response_three.content)
                    unpack_three = unpack_three.decode('utf-8')
                    unpack_three = json.loads(unpack_three)['message']
                    unpack_three = json.loads(unpack_three)
                    exit(unpack_three)

                else:
                    exit("\n\n /token Error : " + str(response_two.status_code))

            else:
                exit("\n\n /did Error : " + str(response_one.status_code) + " - " + str(response_one.content.decode()))

        except IndyError as e:
            print('Error occurred: %s' % e)

    async def get_credential(self):

        try:
            # Emanuel Steps
            print("1- The client should have an Indy wallet")
            await wallet.create_wallet(self.prover['wallet_config'], self.prover['wallet_credentials'])

            print('2- Then the wallet should be opened')
            self.wallet_handle = await wallet.open_wallet(self.prover['wallet_config'], self.prover['wallet_credentials'])

            print('3- The client now creates a DID, verkey (public key) and a private key and stores them in the wallet')
            did_json = json.dumps({})
            _did_, _verkey_ = await did.create_and_store_my_did(self.wallet_handle, did_json)

            print("DID : " + _did_)
            print("VerKey : " + _verkey_)

            print('4- The client must also create a master secret')
            # await anoncreds.prover_create_master_secret(wallet_handle, self.master_secret_id)

            print("5- The owner must create a credential offer and send it to the client.")
            schema = {
                'name': 'gvt',
                'version': '1.0',
                'attributes': '["age", "sex", "height", "name"]'
            }
            _schema_id_, _schema_ = await anoncreds.issuer_create_schema(
                _did_,
                schema['name'],
                schema['version'],
                schema['attributes']
            )

            cred_def = {
                'tag': 'cred_def_tag',
                'type': 'CL',
                'config': json.dumps({"support_revocation": False})
            }

            await anoncreds.prover_create_master_secret(self.wallet_handle, self.master_secret_id)

            self.cred_offer = input("CREDENTIAL OFFER: ")
            self._cred_def_ = input("CREDENTIAL DEFINITION:")

            cred_req, cred_req_metadata = await anoncreds.prover_create_credential_req(
                self.wallet_handle,
                _did_,
                self.cred_offer,
                self._cred_def_,
                self.master_secret_id
            )

            print(cred_req)
            self.myCredit = input("CREDENTIAL: ")

            outPut = await anoncreds.prover_store_credential(
                self.wallet_handle,
                "69aWwGn8QxWG2HjYb8E4SY:3:CL:100:thing_cdef",
                cred_req_metadata,
                self.myCredit ,
                self._cred_def_,
                None
            )

            # Close & Delete The Wallet
            await wallet.close_wallet(self.wallet_handle)
            # await wallet.delete_wallet(self.wallet_config, self.wallet_credentials)
        except IndyError as e:
            print('Error occurred: %s' % e)
