pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Meliodaus957/Project-Work.git' // Укажи свой репозиторий
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate  # Активируем виртуальное окружение
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate  # Снова активируем виртуальное окружение перед запуском тестов
                    pytest tests --junit-xml=junit.xml --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }
}
