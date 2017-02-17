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
if(empty($_POST['Date']))
	header("Location: ./curated.php");
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
                    <li>
                        <a href="admin_dash.php"><i class="fa fa-fw fa-dashboard"></i> Dashboard</a>
                    </li>
                    <li>
                        <a href="admin_charts.php"><i class="fa fa-fw fa-bar-chart-o"></i> Charts</a>
                    </li>
                    <li>
                        <a href="upload_csv.php"><i class="fa fa-fw fa-file"></i> Upload CSV File</a>
                    </li>
                    <li <?php if($_POST["Curated"]==3) echo "class='active'"; ?> >
                        <a <?php if($_POST["Curated"]==3) echo "style='background-color:#080808;'" ?> href="curated.php"><i class="fa fa-fw fa-file"></i>Non Curated</a>
                    </li>
                    <li  <?php if($_POST["Curated"]==1) echo "class='active'"; ?>>
                        <a <?php if($_POST["Curated"]==1) echo "style='background-color:#080808;'" ?> href="partial_curated.php"><i class="fa fa-fw fa-file"></i>Partially Curated</a>
                    </li>
                    <li  <?php if($_POST["Curated"]==2) echo "class='active'"; ?>>
                        <a <?php if($_POST["Curated"]==2) echo "style='background-color:#080808;'" ?> href="fully_curated.php"><i class="fa fa-fw fa-file"></i>Fully Curated</a>
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
                            Edit Record
                            <small>Editing Data into the database</small>
                        </h1>
                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard"></i>  <a href="admin_dash.php">Dashboard</a>
                            </li>
                            <li>
                                <i class="glyphicon glyphicon-upload"></i>  <a href=<?php if($_POST["Curated"]==3) echo $_SERVER['HTTP_REFERER']; ?>
                              //  else if($_POST["Curated"]==2) echo "fully_curated.php";
                             //   else if($_POST["Curated"]==1) echo "partial_curated.php"; ?> ShowFiles</a>
                            </li>
                            <li class="active">
                                <i class="glyphicon glyphicon-upload"></i>EditFiles
                            </li>
                        </ol>
                    </div>

                </div>

                <!-- /.row -->
                <table width=100% align='center'>
					<tr>
					<td style="padding: 10px">
<!--                <div style="width: 40%; float: left">-->
                <form method=post action=edit_query_process.php>
		

					 <input type='url' style='display: none' name='SourceLink' value= '<?php echo $_POST['SourceLink'] ?>' /> 
					<table width=100% align='center'>						
						<tr>
							<td>Date of release</td>
							<td> <input type='text' name='Date' value= '<?php echo $_POST['Date'] ?>'> </td>
						</tr>
						<tr>
							<td>Price Target (in USD)</td>
							<td><input type='text' name='TP' value= '<?php echo $_POST['TP'] ?>' /></td>
						</tr>
						<tr>
							<td>CMP (in USD)</td>
							<td><input type='text' name='CMP' value= '<?php echo $_POST['CMP'] ?>' /></td>
						</tr>
						<tr>
							<td>Company Name</td>
							<td><input type='text' name='Company_Name' value= '<?php echo $_POST['Company_Name'] ?>' /></td>
						</tr>

						<tr>
							<td>Company Ticker</td>
							<td><input type='text' name='TICKER' value= '<?php echo $_POST['TICKER'] ?>' /></td>
						</tr>

						<tr>
							<td>Firm Name</td>
							<td><input type='text' name='FirmName' value= '<?php echo $_POST['FirmName'] ?>' /></td>
						</tr>
						<tr>
							<td>Sector</td>
							<td><input type='text' name='Sector' value= '<?php echo $_POST['Sector'] ?>' /></td>
						</tr>
						<tr>
							<td>Industry</td>
							<td><input type='text' name='Industry' value= '<?php echo $_POST['Industry'] ?>' /></td>
						</tr>
						<tr>
							<td>Original Recommendation</td>
							<td><input type='text' name='RecoAction_orig' value= '<?php echo $_POST['RecoAction_orig'] ?>' /></td>
						</tr>
						<tr>
							<td>MilkorWater Recommendation</td>
							<td><input type='text' name='RecoAction_Mow' value= '<?php echo $_POST['RecoAction_Mow'] ?>' /></td>
						</tr>
						<tr>
							<td>Analyst First Name</td>
					<td><input type='text' name='Analyst F name' value= '<?php echo $_POST['Analyst_F_name'] ?>' /></td>
						</tr>
						<tr>
							<td>Analyst Last Name</td>
					<td><input type='text' name='Analyst L name' value= '<?php echo $_POST['Analyst_L_name'] ?>' /></td>
						</tr>
						<tr>
							<td>Analyst tc</td>
							<td><input type='text' name='Analyst tc' value= '<?php echo $_POST['Analyst_tc'] ?>' /></td>
						</tr>
						<tr>
							<td>Analyst Email</td>
							<td><input type='text' name='Analyst email' value= '<?php echo $_POST['Analyst_email'] ?>' /></td>
						</tr>
						<tr>
							<td>Horizon</td>
							<td><input type='text' name='Horizon' value= '<?php echo $_POST['Horizon'] ?>' /></td>
						</tr>
						<tr>
							<td>Notes</td>
							<td><input type='text' name='notes' value= '<?php echo $_POST['notes'] ?>' /></td>
						</tr>
						<tr>
							<td>Status</td>
							<td><input type='text' name='Status' value= '<?php echo $_POST['Status'] ?>' /></td>
						</tr>
						<tr>
							<td>Curated</td>
							<td>
								<input type='radio' name='Curated' value=3 required <?php if($_POST["Curated"]==3) echo "checked"; ?>/>No<br>
								<input type='radio' name='Curated' value=1 <?php if($_POST["Curated"]==1) echo "checked"; ?>/>Partially<br>
								<input type='radio' name='Curated' value=2 <?php if($_POST["Curated"]==2) echo "checked"; ?>/>Yes<br>
							</td>
						</tr>
						<tr>
							<td colspan=2 align='center'>
								<input type='submit' value='Save Changes'/>
								<input type='button' value='Cancel' <?php if($_POST["Curated"]==3) echo "onclick=window.location='curated.php'";
								 //echo $_SERVER['HTTP_REFERER'];
								else if($_POST["Curated"]==2) echo "onclick=window.location='fully_curated.php'";
								else if($_POST["Curated"]==1) echo "onclick=window.location='partial_curated.php'"; ?> />
							</td>
						</tr>
				<!--		 <a href=<?php echo $_SERVER['HTTP_REFERER']; ?> > Goto Previous page </a> -->

					
                </form>					<form method = post action=delete_query_process.php>
							<tr>
							
								 <input type='url' style='display: none' name='SourceLink' value= '<?php echo $_POST['SourceLink'] ?>' />
								 <input type='text' style='display: none' name='Curated' value= '<?php echo $_POST['Curated'] ?>' /> 
								<input  type='submit' value='Delete' /> 
							
							</tr>
		  					</form> 
		</table>
<!--                </div>-->
					</td>
					<td style="padding: 10px">
<!--                <div style="width:40%; float: right; margin:20px">        <a href="<?php echo "http://www.someotherwebsite.com"; ?>">  -->
					<p> <a style="valign:top" href= "<?php echo $_POST['SourceLink']; ?>">   Click to go to original Link </a> </p>  

					<textarea rows=25 cols=60 style="valign:top" disabled	><?php echo $_POST['Raw']; ?></textarea>
<!--                </div>-->
					</td>
					</tr>
                </table>



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



