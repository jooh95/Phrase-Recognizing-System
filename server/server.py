from flask import Flask
from flask_restful import Resource, Api, reqparse
import ngrams
from lemma import lemmatize
app = Flask(__name__)
api = Api(app)
import pymongo
mongo_conn = pymongo.MongoClient('mongodb://root:sniperzkzl@localhost:27017')
db = mongo_conn.thesaurus
UserDB = mongo_conn.UserData


def get_name(synset):
    if(type(synset) != int): 
        return {'word':synset.name().partition('.')[0], 'type':synset.name().partition('.')[2][0]}
    return {'word':"None", type:"NotWord"}

def check_string(s):
    flag_first = 0
    flag_last = 0
    if((s[0] >= '0' and s[0] <= '9') or (s[0] >= 'a' and s[0] <= 'z') or (s[0] >= 'A' and s[0] <= 'Z')):
        flag_first = 0
    else:
        flag_first = s[0]
        s = s[1:]
    if((s[-1] >= '0' and s[-1] <= '9') or (s[-1] >= 'a' and s[-1] <= 'z') or (s[-1] >= 'A' and s[-1] <= 'Z')):
        flag_last = 0
    else:
        flag_last = s[-1]
        s = s[0:-1]
    return flag_first, flag_last, s.strip()
    
    


class getData_lstm(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('full_sentence', type=str)
            parser.add_argument('target', type=str)
            args = parser.parse_args()
            _full_sentence = args['full_sentence']
            target = args['target']
            tmp_split = _full_sentence.split(target)
            before_sentences = tmp_split[0].split('.')
            _current_sentence_top = before_sentences[-1]
            _current_sentence_middle = target.split('<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>')[1]
            print(_current_sentence_middle)
            data_list = _current_sentence_top.split(' ')
            print(data_list)
            try:
                while any('' in s for s in data_list):
                    data_list.remove('')
                    print('remove', data_list)
            except Exception as e:
                pass
            print(data_list)
            pred = ngrams.predict_next_lstm(_current_sentence_top, 8)
            print(pred)
            # word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)
            # print(word2vec_pred)
            return {'result' : pred}
        except Exception as e:
            return {'error':str(e)}

class getData_ver2(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('full_sentence', type=str)
            parser.add_argument('target', type=str)
            args = parser.parse_args()
            _full_sentence = args['full_sentence']
            target = args['target']
            tmp_split = _full_sentence.split(target)
            print(tmp_split[0])
            before_sentences = tmp_split[0].split('.')
            print(before_sentences[-1])
            _current_sentence_top = before_sentences[-1].lower()
            _current_sentence_middle = target.split('<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>')[1].lower()
            print(_current_sentence_middle)
            data_list = _current_sentence_top.split(' ')
            flag_first = 0
            flag_last = 0

            try:
                while any('' in s for s in data_list):
                    data_list.remove('')
                    print('remove', data_list)
            except Exception as e:
                pass

            pred = []
            print("len", data_list)
            print("data", _current_sentence_middle)
            _, _, _current_sentence_middle = check_string(_current_sentence_middle)
            if(len(data_list) <= 1 or len(_current_sentence_middle.split(' ')) >= 2):
                pred = []
            else:
                _, _, data_list[-2] = check_string(data_list[-2])
                _, _, data_list[-1] = check_string(data_list[-1])
                pred = ngrams.prediction((data_list[-2], data_list[-1], _current_sentence_middle), 0)
            # print('pred, _current_sentence_middle,', pred, _current_sentence_middle)
            word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)
            print(_current_sentence_middle, len(_current_sentence_middle.split(' ')))
            print("current_top", _current_sentence_top)
            # pred_lstm = ngrams.predict_next_lstm(_current_sentence_top,8)
            pred_lstm=[]
            print(word2vec_pred)
            if type(pred_lstm) is str:
                pred_lstm = []
            return {'result' : pred, 'word2vec':word2vec_pred, 'lstm':pred_lstm}
        except Exception as e:
            return {'error':str(e)}
class getData_ver3(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('full_sentence', type=str)
            parser.add_argument('target', type=str)
            args = parser.parse_args()
            _full_sentence = args['full_sentence']
            target = args['target']
            tmp_split = _full_sentence.split(target)
            # print('tmp_split',tmp_split)
            # tmp_split[0] = lemmatize(tmp_split[0])
            # print('tmp_split', tmp_split)

            before_sentences = tmp_split[0].split('.')
            print(before_sentences[-1])
            _current_sentence_top = before_sentences[-1].lower()
            _current_sentence_top = lemmatize(_current_sentence_top)
            _current_sentence_middle = target.split('<31fe0826-7bb3-444d-8f2e-6ca06ae24e11>')[1].lower()
            _current_sentence_middle = lemmatize(_current_sentence_middle)
            print(_current_sentence_middle)
            data_list = _current_sentence_top.split(' ')
            flag_first = 0
            flag_last = 0

            try:
                while any('' in s for s in data_list):
                    data_list.remove('')
                    print('remove', data_list)
            except Exception as e:
                pass

            pred = []
            print("len", data_list)
            print("data", _current_sentence_middle)
            _, _, _current_sentence_middle = check_string(_current_sentence_middle)
            if(len(data_list) <= 1 or len(_current_sentence_middle.split(' ')) >= 2):
                pred = []
            else:
                _, _, data_list[-2] = check_string(data_list[-2])
                _, _, data_list[-1] = check_string(data_list[-1])
                pred = ngrams.prediction((data_list[-2], data_list[-1]), _current_sentence_middle, 0)
            print("_current_sentence_middle", _current_sentence_middle)
            word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)
            # word2vec_pred = []
            print(_current_sentence_middle, len(_current_sentence_middle.split(' ')))
            print("current_top", _current_sentence_top)
            pred_lstm = ngrams.predict_next_lstm(_current_sentence_top, 8)

            # pred_lstm = []
            print(word2vec_pred)
            if type(pred_lstm) is str:
                pred_lstm = []
            return {'result' : pred, 'word2vec':word2vec_pred, 'lstm':pred_lstm}
        except Exception as e:
            return {'error':str(e)}

class getData(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('before_sentence', type=str)
            parser.add_argument('current_sentence_top', type=str)
            parser.add_argument('current_sentence_middle', type=str)
            parser.add_argument('next_sentence', type=str)
            args = parser.parse_args()
            _before_sentence = args['before_sentence']
            _current_sentence_top = args['current_sentence_top'].lower()
            _current_sentence_middle = args['current_sentence_middle'].lower()
            _next_sentence = args['next_sentence']
            print(_current_sentence_top, _current_sentence_middle)
            
            data_list = _current_sentence_top.split(' ')
            pred = ngrams.prediction((data_list[-2].lower(), data_list[-1].lower(), _current_sentence_middle), 0)

            word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)

            return {'result' : pred, 'word2vec':word2vec_pred}
        except Exception as e:
            return {'error':str(e)}

class pushHistory(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserName', type=str)
            parser.add_argument('before', type=str)
            parser.add_argument('after', type=str)
            # parser.add_argument('current_sentence_top', type=str)
            # parser.add_argument('current_sentence_middle', type=str)
            # parser.add_argument('next_sentence', type=str)
            args = parser.parse_args()
            user_name = args['UserName']
            tmp_history= {'before':args['before'], 'after':args['after']} 
			


            user_collection = UserDB.ChangeLog
            user_history = user_collection.find_one({"user_name" :user_name})
            try:
                user_history = user_history['history']
            except Exception as e:
                return {'error':"not found user"}

            user_history.append(tmp_history)
			
            user_collection.update({'user_name':user_name},{'history' : user_history})

            return {'result': user_history}
        except Exception as e:
            return {'error': str(e)}

class getHistory(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserName', type=str)
            # parser.add_argument('current_sentence_top', type=str)
            # parser.add_argument('current_sentence_middle', type=str)
            # parser.add_argument('next_sentence', type=str)
            args = parser.parse_args()
            user_name = args['UserName']
            user_collection = UserDB.ChangeLog
            user_history = user_collection.find_one({"user_name" :user_name})
            try:
                user_history = user_history['history']
            except Exception as e:
                return {'error':"not found user"}

            return {'result': user_history}
        except Exception as e:
            return {'error': str(e)}

class createUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserName', type=str)
            # parser.add_argument('current_sentence_top', type=str)
            # parser.add_argument('current_sentence_middle', type=str)
            # parser.add_argument('next_sentence', type=str)
            args = parser.parse_args()
            user_name = args['UserName']
            user_collection = UserDB.ChangeLog
            user_collection.insert({'user_name' : user_name, 'history' : []})
            return {'result': 'done'}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(getData, '/data')
api.add_resource(getData_ver2, '/dev/data')
api.add_resource(getData_ver3, '/dev/v3/data')
api.add_resource(getData_lstm, '/lstm/data')
api.add_resource(getHistory, '/history/get')
api.add_resource(createUser, '/history/create')
api.add_resource(pushHistory, '/history/push')
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    ngrams.main(True)
    app.run(host ='0.0.0.0')
