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
                        echo "Sending mail to $MAIL"
                        echo $MAIL > mail.txt
                        cat mail.txt
                        echo "Build Success"
                        '''
                    }
                }
            }
        }
    }
}