pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/poseidon139/aiPRReview',
                    branch: 'main',
                    credentialsId: '6ef0ce35-81fc-4b78-b204-8a151ef447e5'
            }
        }

        stage('PR review check') {
            when {
                expression {
                    return env.CHANGE_ID != null
                }
            }
            steps {
                echo 'Running PRreviewer.py for Pull Request...'
                sh 'python3 PRreviewer.py'
            }
        }
    }
}
