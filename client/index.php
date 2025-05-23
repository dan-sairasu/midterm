<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Travel Booking Platform</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container py-5">
    <h1 class="mb-4 text-center">🌍 Available Travel Packages</h1>


<div class="row mb-4">
  <div class="col-md-3">
    <select id="filterType" class="form-select">
      <option value="destination">Destination</option>
      <option value="price">Price</option>
      <option value="duration">Duration (days)</option>
    </select>
  </div>
  <div class="col-md-6" id="textInputWrapper">
    <input type="text" id="search" class="form-control" placeholder="Search...">
  </div>
  <div class="col-md-3 d-none" id="rangeInputWrapper">
    <div class="input-group">
      <input type="number" id="min" class="form-control" placeholder="Min">
      <input type="number" id="max" class="form-control" placeholder="Max">
    </div>
  </div>
</div>


    <div class="row" id="packages">

    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
