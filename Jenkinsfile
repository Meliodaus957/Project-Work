pipeline {
    agent any

    environment {
        ALLURE_VERSION = '2.32.2'
        ALLURE_HOME = '/opt/allure/bin'
        PATH = "${env.PATH}:${env.ALLURE_HOME}"
    }

    parameters {
        string(name: 'EXECUTOR', defaultValue: 'selenoid', description: 'Адрес Selenoid')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Браузер')
        string(name: 'BV', defaultValue: 'latest', description: 'Версия браузера')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Meliodaus957/Project-Work.git',
                    credentialsId: 'Jenkins'
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

        stage('Set up environment') {
            steps {
                script {
                    // Устанавливаем Docker Compose
                    sh 'apt-get update'
                    sh 'apt-get install -y docker-compose'
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate  # Снова активируем виртуальное окружение перед запуском тестов
                    pytest tests --junit-xml=junit.xml --alluredir=allure-results \
                    --executor=${EXECUTOR} \
                    --browser=${BROWSER} \
                    --bv=${BV}
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // Генерация отчета Allure, путь к результатам должен быть указан правильно
                    sh 'allure generate allure-results --clean -o allure-report'
                }
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

        changed {
            echo 'Pipeline status has changed'
        }
    }
}