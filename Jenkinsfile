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
                    sh 'allure generate allure-results --clean -o allure-report'
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure resultsPath: 'allure-results'
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
