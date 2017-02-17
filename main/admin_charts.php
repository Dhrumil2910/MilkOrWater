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

    <title>Charts</title>

    <!-- Bootstrap Core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="bootstrap-3.0.0/dist/css/sb-admin.css" rel="stylesheet">

    <!-- Morris Charts CSS -->
    <link href="bootstrap-3.0.0/dist/css/plugins/morris.css" rel="stylesheet">

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
                    <li class="active">
                        <a style="background-color:#080808;" href="admin_charts.php"><i class="fa fa-fw fa-bar-chart-o"></i> Charts</a>
                    </li>
                    <li>
                        <a href="upload_csv.php"><i class="fa fa-fw fa-file"></i> Upload CSV File</a>
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
                            Charts
                        </h1>
                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard"></i>  <a href="admin_dash.php">Dashboard</a>
                            </li>
                            <li class="active">
                                <i class="fa fa-bar-chart-o"></i> Charts
                            </li>
                        </ol>
                    </div>
                </div>
                <!-- /.row -->

                <!-- Flot Charts -->
                <div class="row">
                    <div class="col-lg-12">
                        <h2 class="page-header">Company Statistical Charts</h2>
                        <!--p class="lead">Flot is a pure JavaScript plotting library for jQuery, with a focus on simple usage, attractive looks and interactive features. For full usage instructions and documentation for Flot Charts, visit <a href="http://www.flotcharts.org/">http://www.flotcharts.org/</a>.</p-->
                    </div>
                </div>
                <!-- /.row -->

                <!-- /.row -->

                <div class="row">
                    <div class="col-lg-12">
                        <div class="panel panel-green">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="fa fa-bar-chart-o"></i> Market Price</h3>
                            </div>
                            <div class="panel-body">
                                <div id="morris-area-chart"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- /.row -->

                <div class="row">
                    <div class="col-lg-4">
                        <div class="panel panel-yellow">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="fa fa-long-arrow-right"></i> Sector-wise Distribution</h3>
                            </div>
                            <div class="panel-body">
                                <div id="morris-donut-chart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="panel panel-red">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="fa fa-long-arrow-right"></i> Company Price Targets ($)</h3>
                            </div>
                            <div class="panel-body">
                                <div id="morris-bar-chart"></div>
                            </div>
                        </div>
                    </div>
		    <div class="col-lg-4 emp">
                        <div class="panel panel-primary">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="fa fa-long-arrow-right"></i> Volume of Shares Sold(MSFT)</h3>
                            </div>
                            <div class="panel-body">
                                <div id="morris-line-chart"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- /.row -->

            </div>
            <!-- /.container-fluid -->


        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->
           <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
            <p class="divider" style="background-color:black;"></p>
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

    <!-- Flot Charts JavaScript -->
    <!--[if lte IE 8]><script src="js/excanvas.min.js"></script><![endif]-->
    <script src="bootstrap-3.0.0/dist/js/plugins/flot/jquery.flot.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/flot/jquery.flot.tooltip.min.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/flot/jquery.flot.resize.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/flot/jquery.flot.pie.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/flot/flot-data.js"></script>

</body>

</html>
