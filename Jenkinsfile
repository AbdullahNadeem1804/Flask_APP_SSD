pipeline {
    agent any

    environment {
        // In Windows, virtual envs are usually activated via a Scripts folder
        VENV_PATH = "venv\\Scripts\\activate"
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Using checkout scm as we discussed to keep it simple
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest tests/ --doctest-modules --junitxml=junit_report.xml
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
                echo 'Packaging application for Windows...'
                // Using 'tar' (built into modern Windows) to package the app
                bat 'tar -cvf flask_app.tar . --exclude=venv'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Simulating deployment...'
                // Simple directory copy for simulation
                bat '''
                    if not exist "C:\\temp\\flask_deployment" mkdir "C:\\temp\\flask_deployment"
                    copy flask_app.tar "C:\\temp\\flask_deployment\\"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully on Windows!'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for errors.'
        }
    }
}
