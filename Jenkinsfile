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
                echo 'Packaging only source code (skipping venv)...'
                // This packages only .py files and requirements to keep it clean
                bat 'tar -cf flask_app.tar *.py requirements.txt'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Simulating deployment to target directory...'
                bat '''
                    if not exist "C:\\temp\\deploy" mkdir "C:\\temp\\deploy"
                    copy flask_app.tar "C:\\temp\\deploy\\" /Y
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All stages completed.'
        }
        failure {
            echo 'FAILURE: Check the logs above.'
        }
    }
}
