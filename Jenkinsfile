pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "2022bcs0162santoshhrushith/red_wine_predict_jenkins_2022bcs0162"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python scripts/train.py
                    mkdir -p app/artifacts
                    cp outputs/* app/artifacts/
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'
                    env.CURRENT_R2 = metrics.r2.toString()
                    echo "Current R2: ${env.CURRENT_R2}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {
                        if (env.CURRENT_R2.toFloat() > BEST_ACC.toFloat()) {
                            env.BUILD_IMAGE = "true"
                            echo "Model improved."
                        } else {
                            env.BUILD_IMAGE = "false"
                            echo "Model did not improve."
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.BUILD_IMAGE == "true" }
            }
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", "app")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.BUILD_IMAGE == "true" }
            }
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {

                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                            docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest
                            docker push ${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}