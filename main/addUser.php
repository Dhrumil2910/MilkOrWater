<?php 
session_start();
if($_POST['admin_link']=="admin_dash") header("Location: ./admin_dash.php");
if($_POST['query_link']=="query") header("Location: ./query.php");
if($_POST['Logout']=="logout")
{
	session_destroy();
	header("Location: ./index.php");
}
if($_SESSION['username']==NULL)
{
	$_SESSION['log']=2;
	header("Location: ./index.php");
}
?>
<!DOCTYPE html>  
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Add Users</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="bootstrap-3.0.0/examples/jumbotron/jumbotron.css" rel="stylesheet">
    <!--link href="bootstrap-3.0.0/examples/sticky-footer-navbar/sticky-footer-navbar.css" rel="stylesheet"-->
    <!-- Custom styles for signin template -->
    <link href="bootstrap-3.0.0/customs/footer.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/customs/styles.css"  rel="stylesheet">
    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand">MILKorWATER</a>
        </div>
        <div class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" method="post" role="form">
            <button type="submit" class="btn btn-success" name="admin_link" title="Manage your site" value="admin_dash">Dashboard</button>
            <button type="submit" class="btn btn-primary" name="query_link" title="Query on databse" value="query">
              <i class="glyphicon glyphicon-search"></i></button>
            <button type="submit" class="btn btn-primary" name="new_user" title="Create new users" value="new_user">
              <img src="bootstrap-3.0.0/img/new_user.png" style="width:20px; height:20px;"></button>
            <p class="navbar-text navbar-right" style="line-height:0;"><?php echo $_SESSION['username']?></p>
            <button type="submit" name="Logout" value="logout" id="logstatus" title="Logout" class="btn btn-default">
              <i class="glyphicon glyphicon-log-out"></i></button>
          </form>
        </div><!--/.navbar-collapse -->
    </div>
 
  
    <!-- Sign Up form -->
   <div class="container">
    <h2>Create Account</h2>
    <div class="col-md-6">
     <img src="bootstrap-3.0.0/img/stockmarket1.jpg" style="width:300px; height:300px">
     <img src="bootstrap-3.0.0/img/thinkingman1.jpeg" styke="height: 300px">
    </div>
    <div class="col-md-6"> 
     <form class="regclass" method="post">
        <label>Name</label><br>
        <input type="text" class="Fname" name="fname" placeholder="First Name" required/>
        <input type="text" class="Lname" name="lname" placeholder="Last Name" /><br>
        <br><label>Username</label>
        <i class="glyphicon glyphicon-user"></i><br>
        <input type="text" placeholder="UserName" name="username" required/><br>
        <br><label>Password</label>
        <i class="glyphicon glyphicon-lock"></i><br>
        <input type="password" placeholder="*******" name="password" required/><br>
        <br><label>Confirm Password</label><br>
        <input type="password" placeholder="*******"/ name="passwordc" required/><br>
        <button type="submit" name="regbutton" value="register" class="btn btn-primary regbutton">REGISTER</button>
     </form>
     <?php 
	
	$_SESSION["err"] = NULL;
	if($_POST["regbutton"] == "register")
	{
		
		if( strlen($_POST["username"]) < 6)
		{
			$_SESSION["err"] = "Username must be atleast 6 characters";
		}
		if(!ctype_alnum($_POST["username"]) and $_SESSION["err"] == NULL) 
		{
			$_SESSION["err"] = "Username must be alphanumeric";
		}
		if( strlen($_POST["password"]) < 6 and $_SESSION["err"] == NULL) 
		{
			$_SESSION["err"] = "Password must be atleast 6 characters";
		}
		if( $_POST["password"] != $_POST["passwordc"] and $_SESSION["err"] == NULL)
		{
			$_SESSION["err"] = "Passwords don't match !";
		}
		if($_SESSION["err"] == NULL) 
		{
			$m = new MongoClient();
			$db = $m->ssad;
			$col = $db->users;
			$query = array('username' => $_POST["username"]);
			$proj = array("_id" => false, "username" => true);
			$len = $col->find($query, $proj)->count();
			if ($len >= 1)
			{
				$_SESSION["err"] = "Username already in use";
			}
			else 
			{
				$doc = array(
						"Fname" => $_POST["fname"], 
						"Lname" => $_POST["lname"],
						"username" => $_POST["username"],
						"password" => $_POST["password"]
					);
				$col->insert($doc);
			}
		}		
	}
	if( $_SESSION["err"] != NULL):
     ?>
        <div class="alert alert-danger alert-error" id="alert_form">
         <a href="#" class="close" data-dismiss="alert">&times</a>
         <strong><?php echo $_SESSION["err"] ?></strong>
        </div>
        <script>
         $("#alert_form").css("opacity", 1);
	 console.log( <?php echo $_SESSION["err"] == NULL; ?>);
        </script> 
	<?php endif; ?>
	
    </div>
   </div>

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
  </body>
</html>


