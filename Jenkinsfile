pipeline {
    agent { 
        node {
            label 'docker-agent-alpine-node-python'
            }
      }
    triggers {
        pollSCM('* * * * *')
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
                script {
                    withCredentials([file(credentialsId: 'mailing', variable: 'MAIL')]) {
                        echo "Delivering.."
                        sh '''
                        . venv/bin/activate
                        cp $MAIL/.env .env
                        ls -al
                        python3 mail.py
                        echo "Build Success"
                        '''
                    }
                }
            }
        }
    }
}