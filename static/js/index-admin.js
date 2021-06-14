function addRowToQuotes()
{
  table = document.getElementById('QuotesTable');
  rowCount = table.rows.length;
  row = table.insertRow(rowCount);
  tcell = row.insertCell(0);
  tcell.contentEditable = true;
  tcell = row.insertCell(1);
  tcell.contentEditable = true;
  tcell = row.insertCell(2);
  tcell.innerHTML = '<i class="fas fa-times custom-icon-delete" onclick="deleteRowFromQuotes(this)"></i>';
}

function deleteRowFromQuotes(calle)
{
  calle.parentNode.parentNode.parentNode.removeChild(calle.parentNode.parentNode);
}
