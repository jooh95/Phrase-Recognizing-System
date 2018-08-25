from flask import Flask
from flask_restful import Resource, Api, reqparse
import ngrams
app = Flask(__name__)
api = Api(app)


def get_name(synset):
    if(type(synset) != int): 
        return {'word':synset.name().partition('.')[0], 'type':synset.name().partition('.')[2][0]}
    return {'word':"None", type:"NotWord"}

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
            pred = ngrams.prediction((data_list[-2], data_list[-1], _current_sentence_middle), 0)
            print(pred)
            word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)
            print(_current_sentence_top, len(_current_sentence_middle.split(' ')))
            pred_lstm = ngrams.predict_next_lstm(_current_sentence_top,8)
            print(word2vec_pred)
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
            _current_sentence_top = args['current_sentence_top']
            _current_sentence_middle = args['current_sentence_middle']
            _next_sentence = args['next_sentence']

            data_list = _current_sentence_top.split(' ')
            pred = ngrams.prediction((data_list[-2], data_list[-1], _current_sentence_middle), 0)

            word2vec_pred = ngrams.prediction_by_word2vec(_current_sentence_middle)

            return {'result' : pred, 'word2vec':word2vec_pred}
        except Exception as e:
            return {'error':str(e)}


api.add_resource(getData, '/data')
api.add_resource(getData_ver2, '/dev/data')
api.add_resource(getData_lstm, '/lstm/data')
@app.route('/')
def hello_world():
    ngrams.main(True)
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host ='0.0.0.0')
