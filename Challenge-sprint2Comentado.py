import cv2
import mediapipe as mp
import speech_recognition as sr
import time
import pyttsx3
from datetime import datetime
import requests
import os.path

# insere na variável webcam o frame retirado na camera padrão
# O parâmetro que o vídeoCapture recebe, é o número da webcam que você deseja usar
webcam = cv2.VideoCapture(0)

# utiliza a solução do media pipe que já está pronta
solucao_reconhecimento_rosto = mp.solutions.face_detection

# Aqui é onde recebe a imagem daquele momento e detecta se há um rosto naquela imagem
reconhecedor_de_rostos = solucao_reconhecimento_rosto.FaceDetection()

# Faz o desenho do rosto capturado
desenho = mp.solutions.drawing_utils

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

    # Se o retorno não for um True, o while true é cancelado
    if not verificador:
        break
    # Reconhecer os rostos que tem ali dentro
    lista_rostos = reconhecedor_de_rostos.process(frame)

    # Se detectar algum rosto, é desenhado um quadrado em volta do rosto
    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            # Desenhar os rostos na imagem
            desenho.draw_detection(frame, rosto)

        #Se detectar um rosto, o algoritmo entrara no if e saira do loop infinito
        if lista_rostos.detections:
            time.sleep(3)
            print("Rosto reconhecido")
            break

    # Mostra a imagem capturada e os rostos
    cv2.imshow("Rostos na Webcam", frame)

    # Quando apertar ESC, para o Loop
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

# Criamos uma função que recebe uma fala e transcreve para texto
def sexta_feira_escuta():
    # Utilizamos o método recognizer para escutar o que o usuário está dizendo
    mic = sr.Recognizer()

    # Utilizamos o with para que o código tenha um processo melhor, pois ao final da execução o microfone continua ligado,
    # por isso quando utilizamos o with, ele encerra o microfone e o código ao final da execução
    # Utilizamos o método microphone como source
    with sr.Microphone() as source:
        # Utilizamos o método adjust_for_ambient_noise para melhorar a transcrição da fala em lugares com muito ruído
        mic.adjust_for_ambient_noise(source)
        # Emitimos um print para indicar o começo da transcrição de voz
        print("fale:(vindo da func)")

        # Usamos a variável audio para receber o que o source recebeu
        audio = mic.listen(source)

        try:
            # Dentro de um bloco try, utilizamos o sintetizador do google para transcrever a fala em um texto, colocamos
            # em lower case para evitar erros na comparação e guardamos na variável frase.
            frase = mic.recognize_google(audio, language='pt').lower()
            # Mostramos o texto reconhecido
            print("Texto reconhecido: " + frase)

        # Caso haja algum erro, o algoritmo entra no except
        except sr.UnknownValueError:
            print("Não entendi")
        # Caso a frase seja sintetizada com sucesso, a função retorna a frase
        return frase


# Criamos uma função para buscar os dados do clima em uma api
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

# Criamos uma funcao para o algoritmo falar a data atual
def data_atual():
    #Dicionario contendo os meseses e os respectivos valores como chaves do dicionario
    meses = {1: "Janeiro", 2: "fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho",
             8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

    #variavel recebendo do datetime o dia atual
    dia = datetime.today().day

    #Se valor retornado do metodo today().month estiver na chave de meses, entao:
    if datetime.today().month in meses.keys():
        #variavel mes recebe o valor da chave referente ao today().month
        mes = meses.get(datetime.today().month)

    #Variavel ano recebendo o ano atual
    ano = datetime.today().year

    #String recebendo os valores das variaveis
    texto = "hoje é dia " + str(dia) + " do mês de " + str(mes) + " do ano " + str(ano)

    # Retorno do texto
    return texto

#Criamos uma funcao que retorna o horario atual
def horas():
    #variavel agora recebendo o horario atual
    agora = datetime.now()

    #Variavel hora recebendo a hora
    hora = agora.hour
    #variavel minuto recebendo os minutos
    minuto = agora.minute

    #String recebendo as variaveis
    texto = "Agora são " + str(hora) + " horas e " + str(minuto) + " minutos"

    #Retorno do texto
    return texto

#Na variavel sextaFeira iniciamos o pyttsx3
sextaFeira = pyttsx3.init()

#Setamos os valores (voice para idioma, rate para velocidade da fala, volume para volume)
sextaFeira.setProperty('voice', b'brasil')
sextaFeira.setProperty('rate', 250)
sextaFeira.setProperty('volume', 1)

#Utilizamos um loop para esperar o comando certo vindo do usuario
while True:
    #na variavel resultado guardamos o texto retornado da funcao sexta_feira_escuta()
    resultado = sexta_feira_escuta()

    #Se o valor do resultado for igual a (ok sexta feira) ou (ok sexta-feira)
    if resultado == "ok sexta feira" or resultado == "ok sexta-feira":
        #utilizando a sextaFeira colocamos um audio
        sextaFeira.say("Salve mestre, o que deseja? ")
        sextaFeira.runAndWait()

        #Loop infinito para esperar o comando que o usuario deseja
        while True:
            #na variavel resp guardamos a frase retornada da funcao sexta feira
            resp = sexta_feira_escuta()

            # cadastro de evento
            if resp == "cadastrar evento na agenda":
                #Com o with open, criamos um arquivo txt com o parametro a de 'append' para adicionar as frases no final
                #de cada linha
                #estabelecemos o padrao utf-8 para aceitar caracteres especiais
                with open("agenda.txt", 'a', encoding="utf-8") as f:
                    #Com a sextaFeira fazemos a sextaFeira  falar a string
                    sextaFeira.say("Ok, qual evento devo cadastrar? ")
                    #Colocamos o metodo run and wait para que a fala possa ser reproduzida adequadamente
                    sextaFeira.runAndWait()

                    # na variavel resp guardamos a frase retornada da funcao sexta feira
                    resp = sexta_feira_escuta()

                    #No arquivo recebido como 'f' escrevemos o que foi passado na variavel resp
                    f.write(resp)
                    f.write("\n")

                    #Com a sextaFeira fazemos a sextaFeira  falar a string
                    sextaFeira.say("Evento cadastrado com sucesso! O senhor deseja mais alguma coisa?")
                    #Colocamos o metodo run and wait para que a fala possa ser reproduzida adequadamente
                    sextaFeira.runAndWait()

                    # na variavel resp guardamos a frase retornada da funcao sexta feira
                    resp = sexta_feira_escuta()

                    #Caso o usuario queira ler a agenda depois que cadastrou o evento ele entra no if
                    if resp == "ler agenda" or resp == "leia agenda":
                        # Com o with open, abrimos o arquivo txt com o parametro r de 'read' para ler o que esta escrito
                        # dentro do arquivo txt
                        # estabelecemos o padrao utf-8 para aceitar caracteres especiais
                        with open("./agenda.txt", 'r', encoding="utf-8") as agendaCadastrada:
                            #na variavel fala com o delimitador ',', transformamos as listas retornadas de agendasCadastradas.readlines()
                            #em uma String
                            fala = ",".join(agendaCadastrada.readlines())
                            #Exibimos no console o que se encontra na variavel fala
                            print(fala)
                            #Com a sexta feira executamos a fala da variavel 'fala'
                            sextaFeira.say(fala)
                            sextaFeira.runAndWait()

                    #Se o usuario disser nao
                    elif resp == "não" or resp == "nao":
                        #Entao a sextaFeira executa uma string e sai do if
                        sextaFeira.say("Ok mestre tenha um bom dia!")
                        sextaFeira.runAndWait()
                        break

                    #Se o usuario disser outra coisa, entao ele encerra o if
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

            # Se o usuario disser o comando "Toque uma musica" entao:
            # toque uma musica
            if resp == "toque uma musica" or resp == "toque uma música":
                #Sexta feira vai responder o comando e executara com a biblioteca os, passamos o caminho de uma musica para tocar(Hardcode)
                sextaFeira.say("Ok mestre, abrindo mídia")
                sextaFeira.runAndWait()
                os.system(r"D:\akon-sryBlameItOnMe.mp3")
                break

            # Perguntando a data atual
            #Se o usuario disser o comando "que dia é hoje" entao:
            if resp == "que dia é hoje?" or resp == "que dia é hoje":
                # Na variavel texto armazenamos o retorno da funcao data_atual()
                texto = data_atual()
                # E fazemos a sextaFeira falar o valor da variavel texto
                sextaFeira.say(texto)
                sextaFeira.runAndWait()
                break

            # perguntando que horas sao
            #Se o usuario disser o comando "que horas são" entao:
            if resp == "que horas são":
                # Na variavel texto armazenamos o retorno da funcao horas()
                texto = horas()
                # E fazemos a sextaFeira falar o valor da variavel texto
                sextaFeira.say(texto)
                sextaFeira.runAndWait()
                break

            # abrir calculadora
            #Se o usuario disser o comando "abra a calculadora" entao:
            if resp == "abra a calculadora" or resp == "abra calculadora":
                sextaFeira.say("A calculadora está aberta, quais números deseja calcular?")
                sextaFeira.runAndWait()
                #Dentro da variavel frase guardamos o valor retornado da funcao sexta_feira_escut()
                frase = sexta_feira_escuta()
                #Na variavel calcular, colocamos uma lista dos valores retornados na varaivel 'frase'
                calcular = frase.split()
                #Se na posicao 1 o valor for igual a multiplicacao entao entra no if
                if calcular[1] == 'x':
                    #Na variavel result, transformamos o valor da posicao 0 e 2 em um int
                    result = int(calcular[0]) * int(calcular[2])
                    #E entao a sextaFeira fala a String com o valor da variavel result
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
            #Se o usuario disser o comando "abra a calculadora" entao:
            if resp == "qual a previsão de hoje":
                # E entao a sextaFeira fala a String
                sextaFeira.say("Olá mestre, de qual cidade o senhor deseja saber o clima?")
                sextaFeira.runAndWait()
                #A variavel resp recebe o texto retornado da funcao sexta_feira_escuta()
                resp = sexta_feira_escuta()
                #na variavel clima passamos a funcao buscar clima recebendo como parametro "resp"
                clima = buscar_clima(resp)
                #Entao a sextaFeira fala o texto retornado na variavel "clima"
                sextaFeira.say(clima)
                sextaFeira.runAndWait()
                break

            #Testar a detecção de rosto
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

