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
                    withCredentials([string(credentialsId: 'mail', variable: 'MAIL'), string(credentialsId: 'pass', variable: 'PASS')]) {
                        echo "Delivering.."
                        sh '''
                        . venv/bin/activate
                        echo "MAIL=$MAIL" > .env
                        echo "PASSWORD=$PASS" >> .env
                        python3 mail.py
                        echo "Build Success"
                        '''
                    }
                }
            }
        }
    }
}