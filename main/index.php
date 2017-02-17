<?php
$m = new MongoClient() or die('no client');
$db=$m->ssad or die('cannot connect to ssad');
$collection=$db->users or die('cannot connect to users');
session_start();
if($_SESSION['log']==1) header("Location: ./admin_dash.php");
if(isset($_POST) && $_POST['submitForm']=="Login")
{
	$username=$_POST['username'];
	$password=$_POST['password'];
	$query=array('username' => $username,'password' => $password);
	$result=$collection->findone($query);
	if(!$result){ 
		$_SESSION['log']=0; 
		$_SESSION['message']="Invalid access";
	//	header("Location: ./index.php");
	}
	else{
		$_SESSION['log']=1; 
		$_SESSION['username']=$username;
		$_SESSION['message']="Successfully logged in";
		header("Location: ./admin_dash.php");
	}
}
else if($_SESSION['log']==0) $_SESSION['log']=-1;
?>

<!DOCTYPE html>  
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Admin Login Portal</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="bootstrap-3.0.0/examples/jumbotron/jumbotron.css" rel="stylesheet">
    <!--link href="bootstrap-3.0.0/examples/sticky-footer-navbar/sticky-footer-navbar.css" rel="stylesheet"-->
    <!-- Custom styles for signin template -->
    <link href="bootstrap-3.0.0/customs/signin.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/customs/footer.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="bootstrap-3.0.0/assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

  <!--  Page Header  -->
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">MILKorWATER</a>
        </div>
        <div class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" role="form">
            <button type="submit" id="logstatus" class="btn btn-default">Login</button>
          </form>
        </div><!--/.navbar-collapse -->
    </div>
 <!--  Page Header Complete  -->

  <!--  Jumbotron  -->
    <div class="jumbotron">
      <div class="container">
        <h1>Hello Admin!</h1>
        <p>Welcome to the Company's Statistical Database Management Portal. Please login through this portal to manage your database or to query over it.</p>
        <!--p><a class="btn btn-primary btn-lg" role="button">Learn more &raquo;</a></p-->
      </div>
    </div>
  <!--  Jumbotron Complete  -->

  <div class="container">
<?php if($_SESSION['log']==0): ?>
    <div class="alert alert-danger alert-error" id="alert_out">
        <a href="#" class="close" data-dismiss="alert">&times;</a>
        <strong>Error!</strong> Invalid Login. Please Try Again.
    </div>
<script>
	$('#alert_out').css('opacity', 1);
</script>
<?php elseif($_SESSION['log']==2): ?>
    <div class="alert alert-danger alert-error" id="alert_in">
        <a href="#" class="close" data-dismiss="alert">&times;</a>
        <strong>Access Denied!</strong> Please login to access previous site.
    </div>
<script>
	$('#alert_in').css('opacity', 1);
</script>
<?php endif; ?>

<!--  Login Form  -->
      <form class="form-signin" method="POST" role="form">
        <h2 class="form-signin-heading">Please sign in</h2>
        <input type="text" name="username" class="form-control" placeholder="Username" required autofocus>
        <input type="password" name="password" class="form-control" placeholder="Password" required>
        <label class="checkbox">
          <input type="checkbox" value="remember-me"> Remember me
        </label>
        <button class="btn btn-lg btn-primary btn-block" name="submitForm" value="Login" type="submit">Sign in</button>
      </form>

    </div> <!-- /container -->
<!--  Login Form Complete  -->


  <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
	    <div class="pull-left"><p>&copy; 2014 MilkorWater</p></div>
	    <div class="pull-right"><p>Build: 1.0 Rev 3933 </p></div>
      </div>
    </div>
  <!-- Footer Complete  -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="./bootstrap-3.0.0/dist/js/1.11.1_jquery.min.js"></script>
    <script src="./bootstrap-3.0.0/dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="./bootstrap-3.0.0/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
<script>
console.log(<?php echo $_SESSION['log']; echo $_SESSION['message'];?>)
console.log("<?php echo $_SESSION['username'];?>")
</script>
