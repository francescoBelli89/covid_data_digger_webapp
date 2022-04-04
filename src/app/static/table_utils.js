document.addEventListener('DOMContentLoaded', function () {
  const table = document.getElementById('covidCasesTable');
  const headers = table.querySelectorAll('th');
  const tableBody = table.querySelector('tbody');
  const rows = tableBody.querySelectorAll('tr');

  // Track sort directions
  const directions = Array.from(headers).map(function (header) {
      return '';
  });

  // Transform the content of given cell in given column
  const transform = function (index, content) {
      // Get the data type of column
      const type = headers[index].getAttribute('data-type');
      switch (type) {
          case 'number':
              return parseFloat(content);
          case 'string':
          default:
              return content;
      }
  };

  const sortColumn = function (index) {
      // Get the current direction
      const direction = directions[index] || 'asc';

      // A factor based on the direction
      const multiplier = direction === 'asc' ? 1 : -1;

      const newRows = Array.from(rows);

      newRows.sort(function (rowA, rowB) {
          const cellA = rowA.querySelectorAll('td')[index].innerHTML;
          const cellB = rowB.querySelectorAll('td')[index].innerHTML;

          const a = transform(index, cellA);
          const b = transform(index, cellB);

          switch (true) {
              case a > b:
                  return 1 * multiplier;
              case a < b:
                  return -1 * multiplier;
              case a === b:
                  return 0;
          }
      });

      // Remove old rows
      [].forEach.call(rows, function (row) {
          tableBody.removeChild(row);
      });

      // Reverse the direction
      directions[index] = direction === 'asc' ? 'desc' : 'asc';

      // Append new row
      newRows.forEach(function (newRow) {
          tableBody.appendChild(newRow);
      });
  };

  [].forEach.call(headers, function (header, index) {
      header.addEventListener('click', function () {
          sortColumn(index);
      });
  });
});
function exportTableToExcel(tableID, filename = ''){
  var downloadLink;
  var dataType = 'data:application/vnd.ms-excel';
  var tableSelect = document.getElementById(tableID);
  var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');
  
  // Specify file name
  filename = filename?filename+'.xls':'excel_data.xls';
  
  // Create download link element
  downloadLink = document.createElement("a");
  
  document.body.appendChild(downloadLink);
  
  if(navigator.msSaveOrOpenBlob){
      var blob = new Blob(['\ufeff', tableHTML], {
          type: dataType
      });
      navigator.msSaveOrOpenBlob( blob, filename);
  }else{
      // Create a link to the file
      downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
  
      // Setting the file name
      downloadLink.download = filename;
      
      //triggering the function
      downloadLink.click();
  }
};