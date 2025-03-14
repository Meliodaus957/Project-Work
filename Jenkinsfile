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
                git branch: 'main',
                    url: 'https://github.com/Meliodaus957/Project-Work.git',
                    credentialsId: 'Jenkins'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install --upgrade webdriver-manager
                    pip install allure-pytest

                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests --junit-xml=junit.xml --alluredir=allure-results
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
                script {
                    allure([
                        results: [[path: 'allure-results']]
                        report: [['allure-report']]
                    ])
                }
            }
        }
    }

    post {
        always {
            junit '**/junit.xml'

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
            echo '✅ Pipeline успешно выполнен!'
        }

        failure {
            echo '❌ Pipeline завершился с ошибками!'
        }

        unstable {
            echo '⚠️ Pipeline нестабильный!'
        }
    }
}
