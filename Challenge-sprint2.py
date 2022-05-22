import cv2
import mediapipe as mp
import speech_recognition as sr
import time
import pyttsx3
from datetime import datetime
import requests
import os.path

webcam = cv2.VideoCapture(0)

solucao_reconhecimento_rosto = mp.solutions.face_detection

reconhecedor_de_rostos = solucao_reconhecimento_rosto.FaceDetection()

desenho = mp.solutions.drawing_utils

while True:

    verificador, frame = webcam.read()

    if not verificador:
        break
    lista_rostos = reconhecedor_de_rostos.process(frame)

    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            desenho.draw_detection(frame, rosto)

        if lista_rostos.detections:
            time.sleep(3)
            print("Rosto reconhecido")
            break

    cv2.imshow("Rostos na Webcam", frame)

    if cv2.waitKey(5) == 27:
        break

webcam.release()
cv2.destroyAllWindows()

print("Aqui comeca o projeto sexta-feira")

'''
    Depois que o algoritmo detecta um rosto, ele espera 3 segundos e sai do loop infinito utilizado
    para localizar um rosto.
    A partir daqui, o algoritmo do projeto sexta-feira é inicializado.
'''


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


def buscar_clima(cidade):
    API_KEY = "11c95aecdde84bed43cb10a7c167a494"  # chave api para consultar o clime
    city = cidade  # variável que recebe o parâmetro

    link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pt_br"
    requisicao = requests.get(link)
    dados = requisicao.json()
    descricao = dados['weather'][0]['description']
    temp = round(dados['main']['temp'] - 273.00, 1)

    frase = "Hoje está {} na cidade {} e está fazendo {} graus".format(descricao, city, temp)

    return frase


def data_atual():
    meses = {1: "Janeiro", 2: "fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho",
             8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

    dia = datetime.today().day

    if datetime.today().month in meses.keys():
        mes = meses.get(datetime.today().month)

    ano = datetime.today().year

    texto = "hoje é dia " + str(dia) + " do mês de " + str(mes) + " do ano " + str(ano)

    # Retorno do texto
    return texto


def horas():
    agora = datetime.now()

    hora = agora.hour
    minuto = agora.minute

    texto = "Agora são " + str(hora) + " horas e " + str(minuto) + " minutos"

    return texto


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

                    elif resp == "não" or resp == "nao":
                        sextaFeira.say("Ok mestre tenha um bom dia!")
                        sextaFeira.runAndWait()
                        break
                    else:
                        sextaFeira.say("O comando cadastrar evento encerrou")
                        sextaFeira.runAndWait()
                        break

            # Ler agenda (if opcional)
            if resp == "ler agenda" or resp == "leia agenda":

                if not os.path.exists("./agenda.txt"):
                    sextaFeira.say("o senhor ainda não cadastrou nenhum evento na agenda!")
                    sextaFeira.runAndWait()
                    break
                else:
                    with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                        fala = ",".join(agendaCadastrada.readlines())
                        print(fala)
                        sextaFeira.say(fala)
                        sextaFeira.runAndWait()
                        break

            # toque uma musica
            if resp == "toque uma musica" or resp == "toque uma música":
                sextaFeira.say("Ok mestre, abrindo mídia")
                sextaFeira.runAndWait()
                os.system(r"D:\akon-sryBlameItOnMe.mp3")
                break

            # Perguntando a data atual
            if resp == "que dia é hoje?" or resp == "que dia é hoje":
                texto = data_atual()
                sextaFeira.say(texto)
                sextaFeira.runAndWait()
                break

            # perguntando que horas sao
            if resp == "que horas são":
                # Na variavel texto armazenamos o retorno da funcao horas()
                texto = horas()
                # E fazemos a sextaFeira falar o valor da variavel texto
                sextaFeira.say(texto)
                sextaFeira.runAndWait()
                break

            # abrir calculadora
            if resp == "abra a calculadora" or resp == "abra calculadora":
                sextaFeira.say("A calculadora está aberta, quais números deseja calcular?")
                sextaFeira.runAndWait()
                frase = sexta_feira_escuta()
                calcular = frase.split()
                if calcular[1] == 'x':
                    result = int(calcular[0]) * int(calcular[2])
                    sextaFeira.say("O resultado é: {}".format(result))
                    sextaFeira.runAndWait()
                elif calcular[1] == '+':
                    result = int(calcular[0]) + int(calcular[2])
                    sextaFeira.say("O resultado é: {}".format(result))
                    sextaFeira.runAndWait()
                elif calcular[1] == '-':
                    result = int(calcular[0]) - int(calcular[2])
                    sextaFeira.say("O resultado é: {}".format(result))
                    sextaFeira.runAndWait()
                else:
                    result = int(calcular[0]) / int(calcular[2])
                    sextaFeira.say("O resultado é: {}".format(result))
                    sextaFeira.runAndWait()
                break

            # consultar o clima
            if resp == "qual a previsão de hoje":
                sextaFeira.say("Olá mestre, de qual cidade o senhor deseja saber o clima?")
                sextaFeira.runAndWait()
                resp = sexta_feira_escuta()
                clima = buscar_clima(resp)
                sextaFeira.say(clima)
                sextaFeira.runAndWait()
                break

            #Abrir câmera
            if resp == "abrir camera" or resp == "abrir câmera":
                webcam = cv2.VideoCapture(0)

                solucao_reconhecimento_rosto = mp.solutions.face_detection

                reconhecedor_de_rostos = solucao_reconhecimento_rosto.FaceDetection()

                desenho = mp.solutions.drawing_utils

                while True:
                    verificador, frame = webcam.read()

                    if not verificador:
                        break
                    lista_rostos = reconhecedor_de_rostos.process(frame)

                    if lista_rostos.detections:
                        for rosto in lista_rostos.detections:
                            desenho.draw_detection(frame, rosto)

                    cv2.imshow("Rostos na Webcam", frame)

                    if cv2.waitKey(5) == 27:
                        break

                webcam.release()
                cv2.destroyAllWindows()
                break

    else:
        print("Não entendi o que voce disse")
