pipeline {
    agent any

    // Polls GitHub every ~2 minutes. (Replace with githubPush() if you set up a webhook via ngrok.)
    triggers { pollSCM('H/2 * * * *') }

    environment {
    	APP_NAME       = 'php-app-container'
    	IMAGE_NAME     = 'php-app'
    	TEST_CONTAINER = 'php-app-test'
    	TEST_PORT      = '8001'
    	APP_PORT       = '8000'
    	DOCKER_HOST_IP = 'host.docker.internal'
    }

    stages {
        stage('Checkout Code') {
            steps { checkout scm }
        }

        stage('Build Docker Image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:build-${BUILD_NUMBER} .'}
        }

        stage('Run Tests') {
            steps { sh 'docker run --rm ${IMAGE_NAME}:build-${BUILD_NUMBER} php /var/www/tests/run_tests.php'}
        }

        stage('Health Check - New Container') {
            steps {
                sh '''
                    docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                    docker run -d --name ${TEST_CONTAINER} -p ${TEST_PORT}:80 ${IMAGE_NAME}:build-${BUILD_NUMBER}
                    sleep 5
                    HEALTHY=false
                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if curl -sf http://${DOCKER_HOST_IP}:${TEST_PORT}/health.php > /dev/null; then
                            echo "Health check PASSED on attempt $i"
                            HEALTHY=true
                            break
                        fi
                        echo "Health check failed on attempt $i/10"
                        sleep 3
                    done
                    if [ "$HEALTHY" != "true" ]; then
                        docker logs ${TEST_CONTAINER}
                        docker rm -f ${TEST_CONTAINER}
                        exit 1
                    fi
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                    docker rm -f ${APP_NAME} 2>/dev/null || true
                    docker run -d --name ${APP_NAME} -p ${APP_PORT}:80 ${IMAGE_NAME}:build-${BUILD_NUMBER}
                    echo "Deployed on http://localhost:${APP_PORT}"
                '''
            }
        }
    }

    post {
        always {
            // ---- Change Report: what was integrated in this build ----
            withEnv(["BUILD_STATUS=${currentBuild.currentResult}"]) {
                sh 'python3 generate_change_report.py'
            }
            script { currentBuild.description = readFile('reports/summary.txt').trim() }
            publishHTML(target: [
                reportDir: 'reports', reportFiles: 'change_report.html',
                reportName: 'Change Report', keepAll: true,
                alwaysLinkToLastBuild: true, allowMissing: true
            ])
            archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
        }
        success { echo 'Application deployed successfully.' }
        failure { echo 'Pipeline failed - see the Change Report for the commits in this build.' }
    }
}
