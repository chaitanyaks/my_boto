pipeline {
  agent {
    docker {
      label 'slave-1'
    }

  }
  stages {
    stage('stage-1') {
      steps {
        sh 'hostname'
      }
    }
  }
}
