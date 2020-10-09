#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail



print_usage() {
echo "$(basename "$0") - Generate cucushift vars
Usage: $(basename "$0") [options...]
Options:
  --dry-run         If specified, only print the vars that would be used by cucushift, without updating your shell script.
  --update-file|-f  The script will update your exsiting var shell script you specified.
" >&2
}

update_file() {
    echo "input the path of your shell script: "
    read shell_path
    sed -i -r "/ENV_OCP4_HOSTS/s/([a-Z|/b]+=)(.*)/\1$MARSTER:master:node,$LB:lb/" $shell_path
    sed -i -r "/ENV_OCP4_USER_MANAGER_USERS/s/([a-Z|/b]+=)(.*)/\1$USERS/" $shell_path
    sed -i -r "/admin_creds_spec/s|([a-Z|/b]+:)(.*)|\1 \"$KUBE_VIEWLINK\"|" $shell_path
    sed -i -r "/version/s/([a-Z|/b]+:)(.*)/\1 \"$VERSION\"/" $shell_path
    sed -i -r "/idp/s|([a-Z|/b]+:)(.*)|\1 \"$IDP\"|"  $shell_path
    sed -i -r "/admin_console_url/s|([a-Z|/b]+:)(.*)|\1 \"$CONSOLE_ROUTE\"|" $shell_path
    source $shell_path

}
generate_cucushift_vars() {

  echo "+++++++++++++++++++++++cucushift variables+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  echo "export BUSHSLICER_DEBUG_AFTER_FAIL=1"
  echo "export BUSHSLICER_DEFAULT_ENVIRONMENT=ocp4"
  echo "export OPENSHIFT_ENV_OCP4_HOSTS=$MARSTER:master:node,$LB:lb"
  echo "export OPENSHIFT_ENV_OCP4_USER_MANAGER_USERS=$USERS"
  echo "export BUSHSLICER_CONFIG='
  global:
    browser: chrome
  environments:
    ocp4:
      admin_creds_spec: \"$KUBE_VIEWLINK\"
      version: \"$VERSION\"
      idp: \"flexy-htpasswd-provider\"
      admin_console_url: \"$CONSOLE_ROUTE\"
'
"
 
}

init_var() {
  echo "kubeconfig view link:"
  echo "such as: https://openshift-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/job/Launch%20Environment%20Flexy/72875/artifact/workdir/install-dir/auth/kubeconfig/*view*/"
  read KUBE_VIEWLINK
  USER_VIEWLINK=$(echo $KUBE_VIEWLINK |sed -r "s|(^http.*artifact/)(.*)|\1users.spec/*view*/|")
  curl -k -o ./cucushift_kubeconfig $KUBE_VIEWLINK
  curl -k -o ./cucushift_users $USER_VIEWLINK
  echo "which gerneral user you prefer to use?(users in flexy-htpasswd-provider,just input the num[1-49] is ok)"
  read user
  USERS=$(cat ./cucushift_users | awk -F, 'OFS="," {print $"'$user'",$("'$user'"+1)}')
  echo $USERS
  echo "please input version you want running on: 4.1/4.2/4.3/4.4"
  read VERSION
  CONSOLE_ROUTE=$(oc get route -n openshift-console --config=./cucushift_kubeconfig | awk  '$1 ~ /console/{print "https://"$2}')
  MARSTER=$(oc get node -l node-role.kubernetes.io/master --config=./cucushift_kubeconfig | awk 'NR==2{print $1}')
  LB=$(oc get infrastructures.config.openshift.io cluster -o 'jsonpath={.status.apiServerURL}' --config=./cucushift_kubeconfig | sed -e 's|^[^/]*//||' -e 's|:.*$||')
  IDP=flexy-htpasswd-provider
  rm ./cucushift_kubeconfig
  rm ./cucushift_users
}


for i in "$@"
do
case $i in
    --dry-run)
    init_var	    
    generate_cucushift_vars
    ;;
    -h|--help)
      print_usage
      exit 0
    ;;
    -update|--update-file)
      init_var
      update_file
      exit 0
    ;;
    *)
     print_usage
     exit 1
    ;;
esac
done

   
