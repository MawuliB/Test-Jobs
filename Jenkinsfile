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
        echo "${env.GIT_COMMIT}"
        def commitSha = env.GIT_COMMIT
        def repoOwner = env.GITHUB_REPO_OWNER ?: env.GIT_URL?.split('/')[-2]
        def repoName = env.GITHUB_REPO_NAME ?: env.GIT_URL?.split('/')[-1].replaceAll('.git', '')

        if (!commitSha || !repoOwner || !repoName) {
            error "Unable to determine GitHub repository details. Make sure you're using GitHub Branch Source or have configured the necessary environment variables."
        }

        def apiUrl = "https://api.github.com/repos/${repoOwner}/${repoName}/statuses/${commitSha}"
        
        sh """
            curl -H "Authorization: token ${GITHUB_TOKEN}" \
                 -H "Accept: application/vnd.github.v3+json" \
                 -X POST \
                 -d '{"state": "${state}", "context": "continuous-integration/jenkins", "description": "${description}"}' \
                 ${apiUrl}
        """
    }
}