pipeline {
    agent { 
        node {
            label 'docker-agent-alpine-node-python'
        }
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                mkdir .env
                cd app
                pip3 install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                . venv/bin/activate
                cd app
                python3 app.py
                '''
            }
        }
        stage('Deliver') {
            steps {
                withCredentials([file(credentialsId: 'mailing', variable: 'MAIL')]) {
                    echo "Delivering.."
                    sh '''
                    . venv/bin/activate
                    rm -rf .env
                    cp $MAIL .env
                    python3 mail.py
                    '''
                    echo "Build Success"
                }
            }
        }
    }
    post {
        success {
            echo "Build Success"
            githubStatus(
                context: 'continuous-integration/jenkins',
                description: 'The build succeeded!',
                status: 'SUCCESS'
            )
        }
        failure {
            echo "Build Failed"
            githubStatus(
                context: 'continuous-integration/jenkins',
                description: 'The build failed',
                status: 'FAILURE'
            )
        }
    }
}