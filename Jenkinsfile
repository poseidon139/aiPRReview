pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/poseidon139/qAInCICD',
                    branch: 'main',
                    credentialsId: 'github-token'
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
