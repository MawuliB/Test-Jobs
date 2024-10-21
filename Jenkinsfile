pipeline {
    agent { 
        node {
            label any
        }
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
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
        def commitSha = env.GIT_COMMIT
        def repoUrl = env.GIT_URL.replaceAll(/^git@github.com:|.git$/, '')
        def apiUrl = "https://api.github.com/repos/${repoUrl}/statuses/${commitSha}"
        
        sh """
            curl -H "Authorization: token ${GITHUB_TOKEN}" \
                 -H "Accept: application/vnd.github.v3+json" \
                 -X POST \
                 -d '{"state": "${state}", "context": "continuous-integration/jenkins", "description": "${description}"}' \
                 ${apiUrl}
        """
    }
}