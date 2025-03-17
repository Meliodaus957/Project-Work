pipeline {
    agent any

    environment {
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
                    credentialsId: 'Jenkins1'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests --junit-xml=junit.xml
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh 'allure generate allure-results --clean -o allure-report'
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                script {
                    allure([
                        results: [[path: 'allure-results']],
                        report: 'allure-report'
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
                        alwaysLinkToLastBuild: true
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
