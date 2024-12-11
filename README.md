# Story Generator API

Este é um projeto Flask que combina Firebase e Google Generative AI para criar histórias infantis e capas de imagens geradas automaticamente. Além disso, oferece funcionalidades de registro, login e recuperação de histórias armazenadas no Firestore.

## Funcionalidades

1. **Registro de Usuários**:
   - Endpoint: `/register` (POST)
   - Registra um novo usuário no Firebase Authentication com validação de e-mail.
   - Retorna os detalhes do usuário recém-criado.

2. **Login de Usuários**:
   - Endpoint: `/login` (POST)
   - Autentica usuários usando o e-mail e senha registrados.
   - Retorna os detalhes do token decodificado em caso de sucesso.

3. **Geração de Histórias e Capas**:
   - Endpoint: `/generate-story` (POST)
   - Gera uma história infantil criativa com base no título, descrição e atores fornecidos.
   - Cria uma imagem de capa para a história usando uma integração de IA.
   - Armazena os dados no Firestore.

4. **Servir Imagens**:
   - Endpoint: `/images/<filename>` (GET)
   - Permite acessar imagens geradas e armazenadas no diretório definido.

5. **Recuperar Histórias**:
   - Endpoint: `/get-stories` (GET)
   - Retorna todas as histórias armazenadas no Firestore.

## Dependências

- **Backend**: Flask
- **Banco de Dados**: Firestore (Google Firebase)
- **Autenticação**: Firebase Authentication
- **Geração de Conteúdo e Imagens**: Google Generative AI
- **Validação de E-mails**: `email_validator`
