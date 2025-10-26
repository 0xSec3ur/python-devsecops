pipeline {
    agent any
    
    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        VENV_PATH = "${WORKSPACE}/venv"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    echo 'Setting up Python virtual environment...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing Python dependencies...'
                    sh '''
                        . venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running pytest tests...'
                    sh '''
                        . venv/bin/activate
                        pytest -v --junitxml=test-results.xml
                    '''
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    echo 'Running Bandit security scanner...'
                    sh '''
                        . venv/bin/activate
                        bandit -r . -x ./venv,./logs,./.git -f json -o bandit-report.json || true
                        bandit -r . -x ./venv,./logs,./.git || true
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                script {
                    echo 'Scanning Docker image with Trivy...'
                    sh '''
                        trivy image --format json --output trivy-report.json ${IMAGE_NAME}:latest || true
                        trivy image ${IMAGE_NAME}:latest || true
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    echo 'Checking dependencies with Safety...'
                    sh '''
                        . venv/bin/activate
                        safety check --json --output safety-report.json || true
                        safety check || true
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'safety-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo 'Deploying application with Docker Compose...'
                    sh '''
                        # Stop and remove existing containers
                        docker-compose down -v || true
                        
                        # Remove any orphaned containers with the same name
                        docker rm -f flask-devsecops-app || true
                        
                        # Start fresh deployment
                        docker-compose up -d --force-recreate
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo 'Verifying deployment...'
                    sh '''
                        sleep 10
                        curl -f http://localhost:5000/health || exit 1
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}