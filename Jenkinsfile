pipeline {
    agent any

    environment {
        // Указываем путь к установленному Allure (если он установлен вручную)
        ALLURE_HOME = '/opt/allure/bin'
        PATH = "${env.PATH}:${env.ALLURE_HOME}"
        ALLURE_RESULTS = 'allure-results'
        ALLURE_REPORT = 'allure-report'
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
                    pytest tests --junit-xml=junit.xml
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate $ALLURE_RESULTS --clean -o $ALLURE_REPORT'
            }
        }

        stage('Publish Allure Report') {
            steps {
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
