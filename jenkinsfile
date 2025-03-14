pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo.git'
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run UI Tests') {
            steps {
                sh 'pytest tests/ui_tests --alluredir=allure-results'
            }
        }
        stage('Run API Tests') {
            steps {
                sh 'pytest tests/api_tests --alluredir=allure-results'
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
    }
}
