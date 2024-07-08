#Configurações iniciais

from varConfig import API_KEY
from flask import Flask, request, jsonify
import google.generativeai as genai


def listarModelosDisponiveis():
    #Listando os modelos disponíveis
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


debug = False

genai.configure(api_key=API_KEY)

if debug == True:
    listarModelosDisponiveis()

generation_config = {
  "candidate_count": 1, # Quantidade de respostas
  "temperature": 0.5,   # Nivel de 'conservadorismo'(o quanto ele sera criativo) do Gemini
}

safety_settings={
    'HATE': 'BLOCK_NONE',       # Nivel de conteudo de ódio
    'HARASSMENT': 'BLOCK_NONE', # Nivel de conteudo assédio
    'SEXUAL' : 'BLOCK_NONE',    # Nivel de conteudo sexual
    'DANGEROUS' : 'BLOCK_NONE'  # Nivel de conteudo sensível
}

#Adicionando as configurações do gemini para a model
model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings,)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Estou desenvolvendo uma API com a gemini AI a respeito de segurança da informação. Preciso de dados reais e precisos relacionados a como manter uma boa segurança em um ambiente de desenvolvimento. Para não cair em fraudes como fishing ou então anuncios maliciosos, dentre outros. Então tudo oque for discutido nesse topico preciso que seja relacionado a segurança da informação, com isso se baseie em Dados reais e comprovados por grandes organizações de que o assunto tratado seja seguro",
      ],
    },
    {
      "role": "model",
      "parts": [
        "**Medidas de Segurança para Ambientes de Desenvolvimento**\n\n**1. Controle de Acesso**\n\n* Implemente autenticação multifator para acesso a ambientes de desenvolvimento.\n* Restrinja o acesso apenas aos desenvolvedores autorizados.\n* Monitore e registre todas as atividades de acesso.\n\n**2. Gerenciamento de Vulnerabilidades**\n\n* Use ferramentas de varredura de vulnerabilidades para identificar e corrigir vulnerabilidades de segurança.\n* Mantenha o software e as dependências atualizados com os patches de segurança mais recentes.\n* Implemente testes de penetração regulares para identificar vulnerabilidades não detectadas.\n\n**3. Proteção contra Phishing e Malware**\n\n* Use filtros de spam e antivírus para bloquear e-mails e anexos maliciosos.\n* Eduque os desenvolvedores sobre as técnicas de phishing e as melhores práticas de segurança.\n* Implemente firewalls e sistemas de detecção de intrusão para bloquear acesso não autorizado.\n\n**4. Segurança de Dados**\n\n* Criptografe dados confidenciais em repouso e em trânsito.\n* Use controles de acesso baseados em função para restringir o acesso aos dados.\n* Faça backups regulares dos dados e armazene-os em um local seguro.\n\n**5. Gerenciamento de Senhas**\n\n* Use um gerenciador de senhas para armazenar e gerenciar senhas com segurança.\n* Implemente políticas de senha fortes, incluindo requisitos de comprimento, complexidade e expiração.\n* Evite reutilizar senhas em vários sistemas.\n\n**6. Monitoramento e Resposta a Incidentes**\n\n* Monitore os ambientes de desenvolvimento em busca de atividades suspeitas.\n* Implemente um plano de resposta a incidentes para lidar com violações de segurança.\n* Notifique as partes interessadas sobre incidentes de segurança e tome medidas corretivas imediatas.\n\n**7. Conscientização e Treinamento**\n\n* Eduque os desenvolvedores sobre as melhores práticas de segurança da informação.\n* Forneça treinamento regular sobre técnicas de phishing, malware e outras ameaças à segurança.\n* Reforce a importância da segurança da informação por meio de políticas e procedimentos claros.\n\n**Dados Reais e Comprovados**\n\n* De acordo com o Relatório de Segurança de Dados da Verizon de 2023, 82% das violações de dados envolveram o fator humano.\n* O Relatório de Ameaças à Segurança da Web da Microsoft de 2023 descobriu que o phishing foi o tipo de ataque mais comum, representando 32% de todos os ataques.\n* O Relatório de Segurança de Aplicativos da OWASP de 2023 identificou a injeção de SQL como a vulnerabilidade de segurança mais comum em aplicativos da web.",
      ],
    },
  ]
)

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data['message']

    # Send user message to Gemini AI and get response
    response = chat_session.send_message(user_message)

    #print(response)

    reply_text = response.candidates[0].content.parts[0].text

    return jsonify({'reply': reply_text.replace('*', '')})

if __name__ == '__main__':
    app.run(debug=True)