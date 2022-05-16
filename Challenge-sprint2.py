import cv2
import mediapipe as mp
import speech_recognition as sr
import time
import pyttsx3
from datetime import datetime
import requests
import os

#insere na variável webcam o frame retirado na camera padrão
#O parâmetro que o vídeoCapture recebe, é o número da webcam que você deseja usar
webcam = cv2.VideoCapture(0)

#utiliza a solução do media pipe que já está pronta
solucao_reconhecimento_rosto = mp.solutions.face_detection

#Aqui é onde recebe a imagem daquele momento e detecta se há um rosto naquela imagem
reconhecedor_de_rostos = solucao_reconhecimento_rosto.FaceDetection()

#Faz o desenho do rosto capturado
desenho = mp.solutions.drawing_utils

def sexta_feira_escuta():
    mic = sr.Recognizer()

    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        print("fale:(vindo da func)")

        audio = mic.listen(source)

        try:
            frase = mic.recognize_google(audio, language='pt').lower()
            print("Texto reconhecido: " + frase)

        except sr.UnknownValueError:
            print("Não entendi")
        return frase

'''
    Como é retirado um frame (uma foto) por vêz, é necessário que a gente crie um loop
    infinito para que toda fez que um frame seja tirado, o reconhecedor de rosto
    detecte que há um rosto ali dentro
'''
while True:
    '''Ler as informacoes da webcam
    Webcam.read retorna uma informação booleana caso esteja lendo alguma imagem
    e uma lista do frame tirado no momento
    '''
    verificador, frame = webcam.read()

    #Se o retorno não for um True, o while true é cancelado
    if not verificador:
        break
    #Reconhecer os rostos que tem ali dentro
    lista_rostos = reconhecedor_de_rostos.process(frame)

    #Se detectar algum rosto, é desenhado um quadrado em volta do rosto
    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            #Desenhar os rostos na imagem
            desenho.draw_detection(frame, rosto)

        if lista_rostos.detections:
            time.sleep(3)
            break
    #Mostra a imagem capturada e os rostos
    cv2.imshow("Rostos na Webcam", frame)

    #Quando apertar ESC, para o Loop
    if cv2.waitKey(5) == 27:
        break

webcam.release()
cv2.destroyAllWindows()

print("Aqui comeca o o projeto sexta feira")

'''
    Depois que o algoritmo detecta um rosto, ele espera 3 segundos e sai do loop infinito utilizado
    para localizar um rosto.
    A partir daqui, o algoritmo do projeto sexta-feira é inicializado.
'''

#Criamos uma função que recebe uma fala e transcreve para texto
def sexta_feira_escuta():
    #Utilizamos o método recognizer para escutar o que o usuário está dizendo
    mic = sr.Recognizer()

    #Utilizamos o with para que o código tenha um processo melhor, pois ao final da execução o microfone continua ligado,
    #por isso quando utilizamos o with, ele encerra o microfone e o código ao final da execução
    #Utilizamos o método microphone como source
    with sr.Microphone() as source:
        #Utilizamos o método adjust_for_ambient_noise para melhorar a transcrição da fala em lugares com muito ruído
        mic.adjust_for_ambient_noise(source)
        #Emitimos um print para indicar o começo da transcrição de voz
        print("fale:(vindo da func)")

        #Usamos a variável audio para receber o que o source recebeu
        audio = mic.listen(source)

        try:
            #Dentro de um bloco try, utilizamos o sintetizador do google para transcrever a fala em um texto, colocamos
            #em lower case para evitar erros na comparação e guardamos na variável frase.
            frase = mic.recognize_google(audio, language='pt').lower()
            #Mostramos o texto reconhecido
            print("Texto reconhecido: " + frase)

        #Caso haja algum erro, o algoritmo entra no except
        except sr.UnknownValueError:
            print("Não entendi")
        #Caso a frase seja sintetizada com sucesso, a função retorna a frase
        return frase

#Criamos uma função para buscar os dados do clima em uma api
def buscar_clima(cidade):
    API_KEY = "11c95aecdde84bed43cb10a7c167a494" #chave api para consultar o clime
    city = cidade #variável que recebe o parâmetro

    
    link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pt_br"
    requisicao = requests.get(link)
    dados = requisicao.json()
    descricao = dados['weather'][0]['description']
    temp = round(dados['main']['temp'] - 273.00, 1)

    frase = "Hoje está {} na cidade {} e está fazendo {} graus".format(descricao, city, temp)

    return frase


sextaFeira = pyttsx3.init()
sextaFeira.setProperty('voice', b'brasil')
sextaFeira.setProperty('rate', 250)
sextaFeira.setProperty('volume', 1)
while True:
    resultado = sexta_feira_escuta()

    if resultado == "ok sexta feira" or resultado == "ok sexta-feira":
        sextaFeira.say("Salve mestre, o que deseja? ")
        sextaFeira.runAndWait()

        while True:
            resp = sexta_feira_escuta()
            print("depois do while true: ", resp)

            # cadastro de evento
            if resp == "cadastrar evento na agenda":
                with open("agenda.txt", 'a', encoding="utf-8") as f:
                    sextaFeira.say("Ok, qual evento devo cadastrar? ")
                    sextaFeira.runAndWait()

                    resp = sexta_feira_escuta()

                    f.write(resp)
                    f.write("\n")

                    sextaFeira.say("Evento cadastrado com sucesso! O senhor deseja mais alguma coisa?")
                    sextaFeira.runAndWait()

                    resp = sexta_feira_escuta()

                    if resp == "ler agenda" or resp == "leia agenda":
                        with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                            fala = ",".join(agendaCadastrada.readlines())
                            print(fala)
                            sextaFeira.say(fala)
                            sextaFeira.runAndWait()
                            print("passou da leitura")

                    elif resp == "não" or resp == "nao":
                        print(resp)
                        sextaFeira.say("Ok mestre tenha um bom dia!")
                        sextaFeira.runAndWait()

                    else:
                        sextaFeira.say("O comando cadastrar evento encerrou")
                        sextaFeira.runAndWait()

            #Ler agenda (if opcional)
            if resp == "ler agenda" or resp == "leia agenda":
                with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                    fala = ",".join(agendaCadastrada.readlines())
                    print(fala)
                    sextaFeira.say(fala)
                    sextaFeira.runAndWait()

            # toque uma musica
            if resp == "toque uma musica" or resp == "toque uma música":
                sextaFeira.say("Ok mestre, abrindo mídia")
                sextaFeira.runAndWait()
                os.system(r"D:\akon-sryBlameItOnMe.mp3")
                break

            # Perguntando a data atual
            if resp == "que dia é hoje?" or resp == "que dia é hoje":
                meses = {1: "Janeiro", 2: "fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho",
                         8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

                dia = datetime.today().day

                if datetime.today().month in meses.keys():
                    mes = meses.get(datetime.today().month)

                ano = datetime.today().year

                texto = "hoje é dia " + str(dia) + " do mês de " + str(mes) + " do ano " + str(ano)

                sextaFeira.say(texto)
                sextaFeira.runAndWait()

            # perguntando que horas sao
            if resp == "que horas são":
                agora = datetime.now()
                hora = agora.hour
                minuto = agora.minute

                texto = "Agora são " + str(hora) + " horas e " + str(minuto) + " minutos"

                sextaFeira.say(texto)
                sextaFeira.runAndWait()

            # abrir calculadora
            if resp == "abra a calculadora" or resp == "abra calculadora":
                sextaFeira.say("A calculadora está aberta, quais números deseja calcular?")
                sextaFeira.runAndWait()
                frase = sexta_feira_escuta()
                calcular = frase.split()
                if calcular[1] == 'x':
                    result = int(calcular[0]) * int(calcular[2])
                    sextaFeira.runAndWait()
                elif calcular[1] == '+':
                    result = int(calcular[0]) + int(calcular[2])
                    sextaFeira.runAndWait()
                elif calcular[1] == '-':
                    result = int(calcular[0]) - int(calcular[2])
                    sextaFeira.runAndWait()
                else:
                    result = int(calcular[0]) / int(calcular[2])
                    sextaFeira.runAndWait()

            # consultar o clima
            if resp == "qual a previsão de hoje":
                sextaFeira.say("Olá mestre, de qual cidade o senhor deseja saber o clima?")
                sextaFeira.runAndWait()

                resp = sexta_feira_escuta()

                clima = buscar_clima(resp)
                sextaFeira.say(clima)
                sextaFeira.runAndWait()
    else:
        print("Não entendi o que voce disse")

