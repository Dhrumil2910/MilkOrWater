<?php
$m = new MongoClient();
$db=$m->ssad;
$collection=$db->rss;
session_start();
if($_POST['admin_link']=="admin_dash") header("Location: admin_dash.php");
if($_POST['query_link']=="query") header("Location: ./query.php");
if($_POST['new_user']=="new_user") header("Location: ./addUser.php");
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

    <title>Upload CSV</title>

    <!-- Bootstrap Core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.3.2.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="bootstrap-3.0.0/dist/css/sb-admin.css" rel="stylesheet">
    <!-- Morris Charts CSS -->
    <link href="bootstrap-3.0.0/dist/css/plugins/morris.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/customs/upload.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="bootstrap-3.0.0/font-awesome-4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="bootstrap-3.0.0/customs/footer.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <!-- Brand and toggle get grouped for better mobile display -->
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
	        <button type="submit" class="btn btn-success" name="admin_link" title="User Interface" value="admin_dash">Dashboard</button>
	        <button type="submit" class="btn btn-primary" name="query_link" title="Query on databse" value="query">
	        <i class="glyphicon glyphicon-search"></i></button>
	        <button type="submit" class="btn btn-primary" name="new_user" title="Create new users" value="new_user">
	        <img src="bootstrap-3.0.0/img/new_user.png" style="width:20px; height:20px;"></button>
	        <p class="navbar-text navbar-right" style="line-height:0;"><?php echo $_SESSION['username']?></p>
	        <button type="submit" name="Logout" value="logout" id="logstatus" title="Logout" class="btn btn-default">
	        <i class="glyphicon glyphicon-log-out"></i></button>
	      </form>
	    </div><!--/.navbar-collapse -->

            <!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->
                       <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav side-nav">
                    <li class="active">
                        <a  href="admin_dash.php"><i class="fa fa-fw fa-dashboard"></i> Dashboard</a>
                    </li>
                    <li>
                        <a style="background-color:#080808;" href="upload_csv.php"><i class="fa fa-fw fa-file"></i> Upload CSV File</a>
                    </li>
                    <li>
                        <a href="curated.php"><i class="fa fa-fw fa-file"></i>Non Curated</a>
                    </li>
                    <li>
                        <a href="partial_curated.php"><i class="fa fa-fw fa-file"></i>Partially Curated</a>
                    </li>
                    <li>
                        <a href="fully_curated.php"><i class="fa fa-fw fa-file"></i>Fully Curated</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>

        <div id="page-wrapper">

            <div class="container-fluid">

                <!-- Page Heading -->
                <div class="row">
		  <div class="col-lg-12">
                        <h1 class="page-header">
                            Upload CSV
                            <small>Data Insertion into the database</small>
                        </h1>
                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard"></i>  <a href="admin_dash.php">Dashboard</a>
                            </li>
                            <li class="active">
                                <i class="glyphicon glyphicon-upload"></i>  Upload CSV 
                            </li>
                        </ol>
                    </div>

                </div>
                <!-- /.row -->
                <div class="row">
                  <div class="col-lg-12">
                    <div class="panel panel-primary">
                      <div class="panel-heading">
                        <h3 class="panel-title">Upload your CSV file to be imported into the Feeds database</h3>
                      </div>
                    </div>
		    <form method="POST" action="upload.php" enctype="multipart/form-data" name="upload" id="upload"></form>
                    <div class="panel-body">
		      <div class="fileupload fileupload-new" data-provides="fileupload">
                        <span class="btn btn-primary btn-file">
		          <span class="fileupload-new">Select file</span>
                          <span class="fileupload-exists">Change</span>      
		          <input type="file" name="new_file[]" multiple="multiple" form="upload"/>
			</span>
			<span class="fileupload-preview"></span>
    			<a href="#" class="close fileupload-exists" data-dismiss="fileupload" style="float: none">
			  <i class="fa fa-times"></i>
			</a>
  		      </div><!-- file upload -->
		      <button type="submit" class="btn btn-primary" form="upload">Submit</button>
		    </div><!-- panel body -->
                  </div>
                </div>
		<div style="width:50%;" class="container">
		  <?php if($_SESSION["error"] == 3):
		    $_SESSION["error"] = NULL;
		  ?>
		  <div class="alert alert-success" id="upload">
		    <a href="#" class="close" data-dismiss="alert">&times</a>
		    <strong>Success! </strong>Feeds CSV File successfully uploaded in the database.
		  </div>
		  <script>
		    $('#upload').css('opacity', 1);
		  </script>
		  <?php elseif($_SESSION["error"] == 1): 
		    $_SESSION["error"] = NULL; 
		  ?>
		  <div class="alert alert-danger alert-error" id="no_upload">
		    <a href="#" class="close" data-dismiss="alert">&times</a> 
		    <strong>Error!  </strong>File not uploaded. Invalid file format.
		  </div>
		  <script>
		    $('#no_upload').css('opacity', 1);
		  </script>
		  <?php endif; ?>
		</div>

		                <!-- /.row  OF Kartik  -->
                <div class="row">
                  <div class="col-lg-12">
                    <div class="panel panel-primary">
                      <div class="panel-heading">
                        <h3 class="panel-title">Upload your CSV file to be imported into the Company's Database</h3>
                      </div>
                    </div>
		    <form method="POST" action="upload2.php" enctype="multipart/form-data" name="upload2" id="upload2"></form>
                    <div class="panel-body">
		      <div class="fileupload fileupload-new" data-provides="fileupload">
                        <span class="btn btn-primary btn-file">
		          <span class="fileupload-new">Select file</span>
                          <span class="fileupload-exists">Change</span>      
		          <input type="file" name="new_file" form="upload2"/>
			</span>
			<span class="fileupload-preview"></span>
    			<a href="#" class="close fileupload-exists" data-dismiss="fileupload" style="float: none">
			  <i class="fa fa-times"></i>
			</a>
  		      </div><!-- file upload -->
		      <button type="submit" class="btn btn-primary" form="upload2">Submit</button>
		    </div><!-- panel body -->
                  </div>
                </div>
		<div style="width:50%;" class="container">
		  <?php if($_SESSION["error"] == 3):
		    $_SESSION["error"] = NULL;
		  ?>
		  <div class="alert alert-success" id="upload">
		    <a href="#" class="close" data-dismiss="alert">&times</a>
		    <strong>Success! </strong> Company List File successfully uploaded in the database.
		  </div>
		  <script>
		    $('#upload').css('opacity', 1);
		  </script>
		  <?php elseif($_SESSION["error"] == 1): 
		    $_SESSION["error"] = NULL; 
		  ?>
		  <div class="alert alert-danger alert-error" id="no_upload">
		    <a href="#" class="close" data-dismiss="alert">&times</a> 
		    <strong>Error!  </strong>File not uploaded. Invalid file format.
		  </div>
		  <script>
		    $('#no_upload').css('opacity', 1);
		  </script>
		  <?php endif; ?>
		</div>


		</div>
            <!-- /.container-fluid -->
 
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

         <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
            <div class="pull-left"><p>&copy; 2014 MilkorWater</p></div>
            <div class="pull-right"><p>Build: 1.0 Rev 3933 </p></div>
      </div>
    </div>
  <!-- Footer Complete  -->


    <!-- jQuery Version 1.11.0 -->
    <script src="bootstrap-3.0.0/dist/js/jquery-1.11.0.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="bootstrap-3.0.0/dist/js/bootstrap.min.js"></script>

    <!-- Morris Charts JavaScript -->
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/raphael.min.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/morris.min.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/morris-data.js"></script>
    <script src="bootstrap-3.0.0/customs/upload.js"></script>

</body>

</html>
