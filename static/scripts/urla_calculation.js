function expense_sum(sum_obj = '',print_element = '', tag_type=''){ //sum_obj expected to be multiple elements
    var sum = 0;
    if(sum_obj == ''){
       sum = 'error';
    }else{
       sum_obj.each(function(){
          sum += +$(this).val();
       });
    }
    if(print_element != ''){
      if (tag_type == 'value'){
         $(print_element).val(sum);
      }else if (tag_type=='html') {
         $(print_element).html(sum);
      }
       
    }
 }
function phonenumber(inputtxt){
    var phoneno = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if(phoneno.test(inputtxt)){
      return true;
        }
      else
        {
       
        return false;
        }
}

 function date_formating(date=''){
    if (date!=''){
      var formattedDate = new Date(date);
      var d = formattedDate.getDate();
      var m =  formattedDate.getMonth();
      m += 1;  // JavaScript months are 0-11

      var file_dates = (m <= 9 ? '0' + m : m) + '.' + (d <= 9 ? '0' + d : d)
      return file_dates
    }else{
       file_dates = 'error'
    }
  
 }