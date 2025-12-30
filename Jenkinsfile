pipeline {
    agent any

    environment {
        // Define your virtual environment name
        VENV = "venv"
    }

    stages {
        stage('Clone Repository') {
        steps {
            // Replace 'github-repo-creds' with the ID you chose above
            git branch: 'main', 
                credentialsId: 'github-repo-creds', 
                url: 'https://github.com/your-username/your-repo.git'
        }
    }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    # Run pytest and generate a report if needed
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
                echo 'Packaging application...'
                // For Flask, this usually means creating a source distribution or containerizing
                sh 'tar -cvf flask_app.tar.gz .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Simulating deployment...'
                // Example: Copying to a local directory and restarting a service
                sh '''
                    mkdir -p /tmp/flask_deployment
                    cp flask_app.tar.gz /tmp/flask_deployment/
                    # systemctl restart flask_app.service (Requires sudo permissions)
                '''
            }
        }
        
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
