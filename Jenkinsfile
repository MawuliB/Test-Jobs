pipeline {
    agent any

    options {
        // Cleanup workspace before each build
        skipDefaultCheckout(false)
        // Keep only last 5 builds
        buildDiscarder(logRotator(numToKeepStr: '5'))
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
        stage('Cleanup') {
            steps {
                // Clean system memory
                    sh '''
                        set -e

                        # Clear page cache, dentries and inodes
                        sync; echo 3 | tee /proc/sys/vm/drop_caches
                        
                        # Clear swap space
                        swapoff -a && swapon -a
                        
                        # Remove old log files
                        find /var/log -type f -name "*.log" -mtime +7 -exec rm -f {} \\;
                        
                        # Clean temp directories
                        rm -rf /tmp/*
                        rm -rf /var/tmp/*
                        
                        # Clean Jenkins specific directories
                        find ${JENKINS_HOME}/jobs -type d -name "builds" -mtime +7 -exec rm -rf {} +
                        find ${JENKINS_HOME}/jobs -type d -name "workspace" -mtime +7 -exec rm -rf {} +
                    '''
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
        always {
            cleanWs()
        }
    }
}

def updateGitHubStatus(state, description) {
    withCredentials([string(credentialsId: 'Git-token', variable: 'GITHUB_TOKEN')]) {

        def repo = sh(script: 'git config --get remote.origin.url', returnStdout: true).trim()
        def owner = repo.split('/')[3]
        def repoName = repo.split('/')[4]
        
        def apiUrl = "https://api.github.com/repos/${owner}/${repoName}/statuses/${getGitSha()}"
        
        sh """
            curl -H "Authorization: token $GITHUB_TOKEN" \
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
