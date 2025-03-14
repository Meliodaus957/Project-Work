pipeline {
    agent any

    environment {
        ALLURE_VERSION = '2.32.2'
        ALLURE_HOME = '/opt/allure/bin'
        PATH = "${env.PATH}:${env.ALLURE_HOME}"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Meliodaus957/Project-Work.git'
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

        stage('Run UI Tests') {
            steps {
                sh 'pytest tests/ui_tests'
            }
        }

        stage('Run API Tests') {
            steps {
                sh 'pytest tests/api_tests --junit-xml=junit.xml --alluredir=allure-results'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate allure-results --clean -o allure-report'
            }
        }

        stage('Publish Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
                stage('Publish Allure Report') {
            steps {
                // Публикация отчета с использованием плагина Allure Jenkins
                allure(
                    results: [[path: 'allure-results']],
                    report: 'allure-report'
                )
            }
        }
    }

    post {
        always {
            // Отправка junit отчета в Jenkins
            junit '**/junit.xml'

            // Генерация отчета Allure
            script {
                if (fileExists('allure-report')) {
                    publishHTML(target: [
                        reportName: 'Allure Report',
                        reportDir: 'allure-report',
                        reportFiles: 'index.html',
                        keepAll: true,
                        alwaysLinkToLastBuild: false
                    ])
                }
            }
        }

        success {
            echo 'Pipeline succeeded!'
        }

        failure {
            echo 'Pipeline failed!'
        }

        unstable {
            echo 'Pipeline marked as unstable'
        }
    }
}
