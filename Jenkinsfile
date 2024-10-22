pipeline {
    agent { 
        node {
            label 'jenkins-agent-alpine'
        }
    }

    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                echo "$GIT_URL"
                #python3 -m venv venv
                #. venv/bin/activate
                #mkdir .env
                #cd app
                #pip3 install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                #. venv/bin/activate
                #cd app
                #python3 app.py
                '''
            }
        }
        stage('Deliver') {
            steps {
                //withCredentials([file(credentialsId: 'mailing', variable: 'MAIL')]) {
                    echo "Delivering.."
                    sh '''
                    #. venv/bin/activate
                    #rm -rf .env
                    #cp $MAIL .env
                    #python3 mail.py
                    '''
                    echo "Build Success"
               // }
            }
        }
    }
    post {
        success {
            script {
                updateGitHubStatus('success', 'The build succeeded!')
            }
        }
        failure {
            script {
                updateGitHubStatus('failure', 'The build failed')
            }
        }
    }
}

def updateGitHubStatus(state, description) {
    withCredentials([string(credentialsId: 'Git-token', variable: 'GITHUB_TOKEN')]) {
        
        def apiUrl = "https://api.github.com/repos/${env.GIT_URL}/statuses/${getGitSha()}"

        echo "${apiUrl}"
        echo "${getGitUser()}"
        
        sh """
            curl -H "Authorization: token ${GITHUB_TOKEN}" \
                 -H "Accept: application/vnd.github.v3+json" \
                 -X POST \
                 -d '{"state": "${state}", "context": "continuous-integration/jenkins", "description": "${description}"}' \
                 ${apiUrl}
        """
    }
}

def getGitUser() {
    return sh(script: 'git log -1 --pretty=format:%ae', returnStdout: true).trim()
}

def getGitSha() {
    return sh(script: 'git log -n 1 --pretty=format:"%H"', returnStdout: true).trim()
}