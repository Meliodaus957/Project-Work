pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Meliodaus957/Project-Work.git'
            }
        }

        stage('Install Python') {
            steps {
                sh '''
                    apt-get update && apt-get install -y python3 python3-pip python3.11-venv
                '''
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
                script {
                    allure([
                        "allure-results"
                    ])
                }
            }
        }
    }
}
