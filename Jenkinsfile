pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Run Unit Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    python -m pytest --junitxml=junit_report.xml
                '''
            }
            post {
                always {
                    junit 'junit_report.xml'
                }
            }
        }
        stage('Build Application') {
            steps {
                bat 'tar -cvf flask_app.tar . --exclude=venv'
            }
        }
        stage('Deploy') {
            steps {
                bat '''
                    if not exist "C:\\temp\\flask_deployment" mkdir "C:\\temp\\flask_deployment"
                    copy flask_app.tar "C:\\temp\\flask_deployment\\"
                '''
            }
        }
    }
}
