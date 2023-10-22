import json
import nltk
#import string
import random
from youtube_transcript_api import YouTubeTranscriptApi

def lambda_handler(event, context):
    
    nltk.data.path.append("/opt/nltk_data")
    yt_address_param = event['pathParameters']['yt_address']
    #query_params = event['yt_address']
    #query_params = event['address']
    
    address_param = yt_address_param
    #getAdress = event.get('address')
    #getAdress = event.get('address','gsT6eKsnT0M')
    #getAdress = "gsT6eKsnT0M" 
    
    # Get the transcript
    if address_param:
        #srt = YouTubeTranscriptApi.get_transcript(str(getAdress), languages=['en','ja'])#"gsT6eKsnT0M", languages=['en','ja'])#gsT6eKsnT0M은 유튜브 영상 링크이므로 context 매개변수로 교체
        srt = YouTubeTranscriptApi.get_transcript(address_param, languages=['en', 'ja'])

        random_sentence_A = ''
        replaced_sentence_A =''
        replaced_noun_A=''



        # Extract sentences containing nouns
        sentences_with_nouns = []
        for i in range(len(srt)):
            text = srt[i]['text']
            tokens = nltk.word_tokenize(text)
            tagged_words = nltk.pos_tag(tokens)
            noun_tags = ['NN', 'NNP', 'NNS', 'NNPS']
            if any(tag in noun_tags for word, tag in tagged_words):
                sentences_with_nouns.append(text)

        # Choose a random sentence with nouns
        if sentences_with_nouns:
            random_sentence = random.choice(sentences_with_nouns)
            print("문제로 선택된 명사가 포함된 문장 :", random_sentence)
            random_sentence_A = random_sentence
    
        # Replace one noun with an underscore
            tokens = nltk.word_tokenize(random_sentence)
            tagged_words = nltk.pos_tag(tokens)
            replaced_sentence_words = []
            replaced_noun = None
            for word, tag in tagged_words:
                if tag in noun_tags and replaced_noun is None:
                    replaced_sentence_words.append('_' * len(word))
                    replaced_noun = word
                else:
                    replaced_sentence_words.append(word)

            replaced_sentence = ' '.join(replaced_sentence_words)
            print("대체된 문장 :", replaced_sentence)
            replaced_sentence_A = replaced_sentence
    
            if replaced_noun:
                print("대체된 단어 :", replaced_noun)
                replaced_noun_A = replaced_noun
            else:
                print("명사가 없어서 대체된 단어가 없음.")
                replaced_noun_A = 'non'
        else:
            print("명사를 가진 문장이 없음.")
    
            # TODO implement
            #nltk.data.path.append("/opt/python/nltk_data") # this one line fixed it!
            
        json_data = {
                'statusCode': 200,
                'body': json.dumps('youtube translate api with aws lambda!'),
                'urls' : address_param,
                'random_sentence':json.dumps(random_sentence_A, ensure_ascii=False),
                'replaced_sentence_A' : json.dumps(replaced_sentence_A, ensure_ascii=False),
                'replaced_noun_A ' : json.dumps(replaced_noun_A, ensure_ascii=False)
        }
        json_response = json.dumps(json_data, ensure_ascii=False)
        return json_response
    else:
        return {
            'statusCode': 400,
            'body': yt_address_param
        }
        #json.dumps('주소 파라미터가 누락되었습니다.')