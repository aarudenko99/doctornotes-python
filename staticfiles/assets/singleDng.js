/*
 * Author: Chiedo Labs
 * Website: http://labs.chie.do
 */
jQuery(document).ready(function() {
  // Scripts. Encapsulated in an anonymous function to avoid conflicts.
  (function($) {
    /*
    GLOBAL VARIABLES
    */
    dng.variableName = "";
    if(typeof dngJsonData !== 'undefined') dng.parseJsonBody(dngJsonData);
    dng.createForm();
    dng.slideSwitch();
    dng.clickables();
    if($("body").children().hasClass("dngContent")) dng.outputScroll(true);
    count = 0;

    /**
     * Setup clipboard copying
     */
    var buttonCopyToClipboardSelector = '#dngCopyToClipboard';
    if (Clipboard && $(buttonCopyToClipboardSelector) && $(buttonCopyToClipboardSelector).length){
      new Clipboard(buttonCopyToClipboardSelector);
      // Display 'copied to clipboard'
      $(buttonCopyToClipboardSelector).click(function(){
        //alert('Note has been copied to the clipboard.');
      });
    }
  })( jQuery ); // End scripts
});


function setCheckbox () {
  var arr = []
  jQuery('input:checked').each(function () {
    arr.push(`${jQuery(this).attr('name')}||${jQuery(this).val()}`);
  })
  jQuery('#id_checkboxes').val(arr.join(','))
}

/*
NAMESPACE - dng
*/
var dng = {
    /*
     * this function is used to determine if a string is a substring of another
     */
    isSubstring: function(outer, inner) {
      return (function($) { //encapsulated
        outer = outer.toLowerCase();
        inner = inner.toLowerCase();

        if(outer.indexOf(inner) !== -1) return true;
        else return false;
      })( jQuery ); // End scripts
    },

    /*
     * this function is used to handle the initial clicks that would change the output box.
     */
    clickables: function(outer, inner) {
      return (function($) { //encapsulated
        $(".dngCheckBox, .dngCheckBoxMultiline").click(function(){
          var dngContainer = this;
          if($(dngContainer).children().first().is(':checked')){
            $(dngContainer).children().first().attr('checked', false);
            $(dngContainer).css({'background':'#efefef'});
            setCheckbox()
          }
          else{
            $(dngContainer).children().first().attr('checked', 'checked');
            $(dngContainer).css({'background':'#7fbcff'});
            setCheckbox()
          }
          $(".dngOutputContent").empty();
          if($(".HPI").is(":visible")){
            $(".dngOutputContent").append("\r\nHistory of Present Illness\r\n");
            dng.outputBodyPartSwitch('.HPI');
            }
          if($(".Body").is(":visible")){
            $(".dngOutputContent").append("\r\n\r\n");
            dng.outputBodyPartSwitch('.Body');
          }
          if($(".MDM").is(":visible")){
            $(".dngOutputContent").append("\r\nMedical Decision Making\r\n\r\n");
            dng.outputBodyPartSwitch('.MDM');
          }
        });
        $(".dngRadioButton").click(function(){
          var dngContainer = this;
          $(dngContainer).parent().children(".dngRadioButton").css({'background':'#efefef'})
          $(dngContainer).children().first().attr('checked', 'checked');
          $(dngContainer).css({'background':'#edb059'});
          $(".dngOutputContent").empty();
          if($(".HPI").is(":visible")){
            $(".dngOutputContent").append("\r\nHistory of Present Illness\r\n");
            dng.outputBodyPartSwitch('.HPI');
            }
          if($(".Body").is(":visible")){
            $(".dngOutputContent").append("\r\n\r\n");
            dng.outputBodyPartSwitch('.Body');
          }
          if($(".MDM").is(":visible")){
            $(".dngOutputContent").append("\r\nMedical Decision Making\r\n");
            dng.outputBodyPartSwitch('.MDM');
          }
        });
        $(".dngOutputComplete").click(function(){
          $(".dngOutputContent").attr('readOnly', false);
          $(".dngLeftContent").css({'pointer-events': 'none'});
          alert('Feel free to add any additonal comments to your note and copy it to your clipboard.');

        });
      })( jQuery ); // End scripts
    },

    /*
     * This function is used to make the output box scroll along the page.
     */
    outputScroll: function() {
      return (function($) { //encapsulated
        $(window).scroll(function(go){
          if($(window).width()>1100){
            var scroll = $(this).scrollTop();
            var bottom = $("#footer-bottom").offset().top
            var topPush = $(".dngContent").height() - $(".dngOutputBar").height() - 130;

            if(scroll < $(".dngRightContent").offset().top - 125){
              $(".dngOutputBar").css({
                  'position' : 'absolute',
                  'top' : '0',
                  'margin-top':'0'
              });
            }
            else if( bottom <= (scroll + 150 + $(".dngOutputBar").height())){
              $(".dngOutputBar").css({
                  'position' : 'absolute',
                  'top' : '0',
                  'margin-top' : topPush
              });
            }
            else{
              $(".dngOutputBar").css({
                  'position':'fixed',
                  'top':'125px',
                  'margin-top':'0'
              });
            }
          }
        });
      })( jQuery ); // End scripts
    },

    /*
     * This function is used to toggle the view of main sections of the Note then update the output
     */
    slideSwitch: function() {
      return (function($) { //encapsulated
        $(".dngSwitchLeft").hide();
        $("body").on("click", ".dngSwitchButton", function(){
          var button = this;
          $(button).prev().animate({'width':'toggle'},150);
          $(button).next().animate({'width':'toggle'},150);
          $(button).closest(".dngTitleContainer").next().slideToggle();

           $(button).closest(".dngTitleContainer").next().promise().done(function(){
            $(".dngOutputContent").empty();
          if($(".HPI").is(":visible")){
            $(".dngOutputContent").append("\r\nHistory of Present Illness\r\n");
            dng.outputBodyPartSwitch('.HPI');
            }
          if($(".Body").is(":visible")){
            $(".dngOutputContent").append("\r\n\r\n");
            dng.outputBodyPartSwitch('.Body');
          }
          if($(".MDM").is(":visible")){
            $(".dngOutputContent").append("\r\nMedical Decision Making\r\n");
            dng.outputBodyPartSwitch('.MDM');
          }
          });
        });
      })( jQuery ); // End scripts
    },

    /*
     * This function seperates the Json into its three main body parts if it is present in the JSON
     */
    parseJsonBody: function(data) {
      return (function($) { //encapsulated
        var HPI = data["HPI"];
        var Body = data["Body"];
        var MDM = data["MDM"];
        count = 0;

        if(!$.isEmptyObject(HPI)){
          $(".dngContent .pad").append("<div class='card mb-1'> \
                                          <div class='card-header bg-primary-light' role='tab' id='headingHPI'> \
                                            <a class='rotate h5 d-flex justify-content-between mb-0' data-toggle='collapse' href='#collapseHPI' aria-expanded='true' aria-controls='collapseHPI'> \
                                              HPI<i class='material-icons md-24 align-text-bottom'>keyboard_arrow_down</i> \
                                            </a> \
                                          </div> \
                                          <div id='collapseHPI' class='collapse show' role='tabpanel' aria-labelledby='headingHPI'> \
                                            <div class='HPI card-body p-3 mb-0'>");
          $(HPI).each(function(index,bodyType){ dng.parseJsonForms(bodyType, "HPI");});
          $(".dngContent .pad").append("</div></div></div><!-- HPI -->");
        }
        if(!$.isEmptyObject(Body)){
          $(".dngContent .pad").append("<div class='card mb-1'> \
                                          <div class='card-header bg-primary-light' role='tab' id='headingBody'> \
                                            <a class='rotate h5 d-flex justify-content-between mb-0' data-toggle='collapse' href='#collapseBody' aria-expanded='true' aria-controls='collapseBody'> \
                                              Body<i class='material-icons md-24 align-text-bottom'>keyboard_arrow_down</i> \
                                            </a> \
                                          </div> \
                                          <div id='collapseBody' class='collapse show' role='tabpanel' aria-labelledby='headingBody'> \
                                            <div class='Body card-body p-3 mb-0'>");
          $(Body).each(function(index, bodyType){ dng.parseJsonForms(bodyType, "Body");});
          $(".dngContent .pad").append("</div></div></div><!-- Body -->");
        }
        if(!$.isEmptyObject(MDM)){
          $(".dngContent .pad").append("<div class='card mb-1'> \
                                          <div class='card-header bg-primary-light' role='tab' id='headingMDM'> \
                                            <a class='rotate h5 d-flex justify-content-between mb-0' data-toggle='collapse' href='#collapseMDM' aria-expanded='true' aria-controls='collapseMDM'> \
                                              MDM<i class='material-icons md-24 align-text-bottom'>keyboard_arrow_down</i> \
                                            </a> \
                                          </div> \
                                          <div id='collapseMDM' class='collapse show' role='tabpanel' aria-labelledby='headingMDM'> \
                                            <div class='MDM card-body p-3 mb-0'>");
          $(MDM).each(function(index, bodyType){ dng.parseJsonForms(bodyType, "MDM");});
          $(".dngContent .pad").append("</div></div></div><!-- MDM -->")
        }
      })( jQuery ); // End scripts
    },

    /*
     *This function searches through the code passed through it and splits it by the input type
     */
    parseJsonForms: function(bodyType, bodyName) {
      return (function($) { //encapsulated

         for(var index in bodyType) {

           var form = bodyType[index];

            switch(index)
            {
            //Checkboxes
            case "checkBoxes":
              var checkboxes = "";
              $(form.options).each(function(index, checkbox){
                checkboxes += "<div class='dngCheckBox p-2 mr-1 mb-1 mt-0 border-0 rounded'><input type='checkbox' value="+checkbox.value.replace(/ /g,"&#032")+" name='"+bodyName+"CheckBox"+count+"' ><label>"+checkbox.label+"</label></div>";
              });

            $("."+bodyName).append("\
              <div class='dngCheckBoxes' sentence="+form.sentence.replace(/ /g,"&#032")+"> \
              <div class='dngLabel'>"+form.label+"</div> \
              "+checkboxes+" \
              </div><!-- dngCheckboxes-->");
              count++;
              break;

            //Multiline Checkboxes
            case "checkBoxesMultiline":
              var checkboxes = "";
              $(form.options).each(function(index, checkbox){
                checkboxes += "<div class='dngCheckBoxMultiline p-2 mr-1 mb-1 mt-0 border-0 rounded'><input type='checkbox' sentence="+checkbox.sentence.replace(/ /g,"&#032")+" value="+checkbox.value.replace(/ /g,"&#032")+" name='"+bodyName+"CheckBox"+count+"'><label>"+checkbox.label+"</label></div>";
              });

            $("."+bodyName).append("\
              <div class='dngCheckBoxesMultiline'> \
              <div class='dngLabel'>"+form.label+"</div> \
              "+checkboxes+" \
              </div><!-- dngCheckboxesMultiline-->");
              count++;
              break;

            //Radio Buttons
          case "radioButtons":
            var radiobuttons = "";
            $(form.options).each(function(index, radiobutton){
              radiobuttons += "<div class='dngRadioButton'><input type='radio' name='"+bodyName+"Radio"+count+"' value="+radiobutton.value.replace(/ /g,"&#032")+"><label>"+radiobutton.label+"</label></div>"
            });

            $("."+bodyName).append("\
              <div class='dngRadioButtons' sentence="+form.sentence.replace(/ /g,"&#032")+"> \
              <div class='dngLabel'>"+form.label+"</div> \
              "+radiobuttons+" \
              </div><!-- dngRadioButtons-->");
              count++;
              break;

            //text areas
            case "textArea":
              var formValue = form.value.replace(/&#038;/g,'&');
              formValue = formValue.replace(/&#32;/g,' ');
              $("."+bodyName).append("\
              <div class='dngTextArea' sentence="+form.sentence.replace(/ /g,"&#032")+"> \
              <div class='dngLabel'>"+form.label+"</div> \
              <textarea rows='4' col='20' class='dngTextAreaText form-control'>"+formValue+"</textarea> \
              </div><!-- dngTextArea-->");
              break;

            //time frame
            case "timeFrame":
              $("."+bodyName).append("\
                <div class='dngTimeFrame' sentence="+form.sentence.replace(/ /g,"&#032")+"> \
                <div class='dngLabel'>"+form.label+"</div> \
                <input class='dngTimeFrameText' type='text'/> \
                <select> \
                <option value='minutes'>minutes</option> \
                <option value='hours'>hours</option> \
                <option value='days'>days</option> \
                <option value='months'>months</option> \
                <option value='years'>years</option> \
                </select> \
                </div><!— dngTimeFrame —>");
              break;

            //text areas
            case "reminder":
              // for special chars, see: https://tools.oratory.com/altcodes.html.
              var formValue = form.value.replace(/&#038;/g,'&');
              formValue = formValue.replace(/&#32;/g,' ');
              formValue = formValue.replace(/&#10;/g,'\n');
              $("."+bodyName).append("\
              <div class='dngReminder rounded'> \
              <div class='dngLabel'>"+form.label+"</div> \
              <div class='dngReminderText'>"+wpautop(formValue)+"</div> \
              </div><!-- dngReminder-->");
              break;
            }
          }
      })( jQuery ); // End scripts
    },

    /*
     * This function dynamically generates the output to be copied
     */
    createForm: function() {
      return (function($) { //encapsulated
        $("body").on("change", ".dngRadioButtons input, .dngCheckBoxes input, .dngTimeFrame select, .dngCheckBoxesMultiline input", function(){

          $(".dngOutputContent").empty();
          if($(".HPI").is(":visible")){
            $(".dngOutputContent").append("\r\nHistory of Present Illness\r\n");
            dng.outputBodyPartSwitch('.HPI');
            }
          if($(".Body").is(":visible")){
            $(".dngOutputContent").append("\r\n\r\n");
            dng.outputBodyPartSwitch('.Body');
          }
          if($(".MDM").is(":visible")){
            $(".dngOutputContent").append("\r\nMedical Decision Making\r\n");
            dng.outputBodyPartSwitch('.MDM');
          }
        });
        $("body").on("keyup", ".dngTextArea textarea, .dngTimeFrame input", function(){

          $(".dngOutputContent").empty();
          if($(".HPI").is(":visible")){
            $(".dngOutputContent").append("\r\nHistory of Present Illness\r\n");
            dng.outputBodyPartSwitch('.HPI');
            }
          if($(".Body").is(":visible")){
            $(".dngOutputContent").append("\r\n\r\n");
            dng.outputBodyPartSwitch('.Body');
          }
          if($(".MDM").is(":visible")){
            $(".dngOutputContent").append("\r\nMedical Decision Making\r\n");
            dng.outputBodyPartSwitch('.MDM');
          }
        });
      })( jQuery ); // End scripts
    },

    /*
     * This function appends a new sentence to the dngOutputContent
     */
    outputAppend: function(sentence, entry, time, bodyPart){
      return (function($) { //encapsulated
        if(typeof(entry) != "undefined" && entry != ""){
          if(time != "") entry += " " + time;
          sentence = sentence.replace(/{ENTRY}/g, entry);
         if(bodyPart == ".HPI") $(".dngOutputContent").append(sentence + " ");
                else $(".dngOutputContent").append(sentence + "\r\n\r\n");
        }
      })( jQuery ); // End scripts
    },


    /*
     * This funcion switches through the forms ofthe called body part and forms the proper sentence from them.
     */
    outputBodyPartSwitch: function(bodyPart){
      return (function($) { //encapsulated
        $(bodyPart +' > div').each(function(){
          var className = $(this).attr('class');

          switch(className){
          case "dngCheckBoxes":
            var sentence = $(this).attr("sentence");
            var entry = "";
            var checkCount = 0;

             $(this).children(".dngCheckBox").each(function(){
               if($(this).children('input').is(':checked')){
                 if(checkCount == 0){
                   entry = $(this).children('input:checked').val();
                   checkCount++;
                 }
                 else entry += ", " + $(this).children('input:checked').val();
               }
            });

            dng.outputAppend(sentence, entry, "", bodyPart);
            break;

          case "dngCheckBoxesMultiline":
            var entry = "";

            $(this).children('.dngCheckBoxMultiline').each(function(){
              var checkbox = $(this).children('input');

              if($(checkbox).is(':checked')){
                var sentence = "";
                sentence = $(checkbox).attr("sentence");
                entry = $(checkbox).val();

                sentence = sentence.replace(/{ENTRY}/g, entry);
                if(bodyPart == ".HPI") $(".dngOutputContent").append(sentence + " ");
                else $(".dngOutputContent").append(sentence + "\r\n\r\n");
              }
            });
            break;

          case "dngRadioButtons":
            var sentence = $(this).attr("sentence");
            var entry = ""

            entry = $(this).children('.dngRadioButton').children('input:checked').val();

            dng.outputAppend(sentence, entry, "", bodyPart);
            break;

          case "dngTextArea":
            entry = $(this).children('textarea').val().replace(/\n/g,"\r\n");

            if(typeof(entry) != "undefined" && entry != ""){
              if(bodyPart == ".HPI") $(".dngOutputContent").append(entry + " ");
                else $(".dngOutputContent").append(entry + "\r\n\r\n");
            }
            break;

          case "dngTimeFrame":
            var sentence = $(this).attr("sentence");
            var entry = "";
            var time = "";

            entry = $(this).children('input').val();
            time = $(this).children('select').children('option:selected').val();

            dng.outputAppend(sentence, entry, time, bodyPart);
            break;
          }
        });
      })( jQuery ); // End scripts
    }
};


