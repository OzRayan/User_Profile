$(document).ready(function(){
 $("#pass").keyup(function(){
  check_pass();
 });
});

function check_pass()
{
 var val=document.getElementById("pass").value;
 var meter=document.getElementById("meter");
 var no=0;

 if(val!="")
 {
  // If the password length is less than or equal to 13
  if(val.length<=13)no=1;

  // If the password length is greater than 14 and contain any lowercase alphabet or any number or any special character
  if(val.length>13 && val.length<20 && (val.match(/[a-z]/) || val.match(/\d+/) || val.match(/[A-Z]/) || val.match(/[ ,.,\,!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)))no=2;

  // If the password length is greater than 14 and must contain alphabets,numbers and special characters
  if(val.length>13 && val.length<20 && val.match(/[a-z]/) && val.match(/[A-Z]/) && val.match(/\d+/) && val.match(/[ ,.,\,!,@,#,$,%,^,&,*,?,_,~,-,(,)]/))no=3;

  // If the password length is greater than 19 and must contain alphabets,numbers and special characters
  if(val.length>19 && val.match(/[a-z]/) && val.match(/[A-Z]/) && val.match(/\d+/) && val.match(/[ ,.,\,!,@,#,$,%,^,&,*,?,_,~,-,(,)]/))no=4;

  if(no==1)
  {
   $("#meter").animate({width:'75px'},300);
   meter.style.backgroundColor="#ff0000";
   document.getElementById("pass_type").innerHTML="Very Weak";
  }

  if(no==2)
  {
   $("#meter").animate({width:'150px'},300);
   meter.style.backgroundColor="#ff8800";
   document.getElementById("pass_type").innerHTML="Weak";
  }

  if(no==3)
  {
   $("#meter").animate({width:'225px'},300);
   meter.style.backgroundColor="#88ff00";
   document.getElementById("pass_type").innerHTML="Good";
  }

  if(no==4)
  {
   $("#meter").animate({width:'300px'},300);
   meter.style.backgroundColor="#00FF00";
   document.getElementById("pass_type").innerHTML="Strong";
  }
 }

 else
 {
  meter.style.backgroundColor="white";
  document.getElementById("pass_type").innerHTML="";
 }
}
