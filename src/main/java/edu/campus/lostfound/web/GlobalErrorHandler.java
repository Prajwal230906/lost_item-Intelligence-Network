package edu.campus.lostfound.web;
import java.util.Map;import java.util.NoSuchElementException;import org.springframework.http.*;import org.springframework.web.bind.MethodArgumentNotValidException;import org.springframework.web.bind.annotation.*;import org.springframework.web.servlet.resource.NoResourceFoundException;
@RestControllerAdvice public class GlobalErrorHandler{
 @ExceptionHandler(MethodArgumentNotValidException.class)ResponseEntity<Map<String,Object>> invalid(MethodArgumentNotValidException ex){return ResponseEntity.badRequest().body(Map.of("error","Validation failed","fields",ex.getBindingResult().getFieldErrors().stream().map(e->Map.of("field",e.getField(),"message",e.getDefaultMessage()==null?"Invalid value":e.getDefaultMessage())).toList()));}
 @ExceptionHandler(NoResourceFoundException.class)ResponseEntity<Map<String,String>> missing(NoResourceFoundException ex){return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error","Resource not found"));}
 @ExceptionHandler(NoSuchElementException.class)ResponseEntity<Map<String,String>> missingRecord(NoSuchElementException ex){return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error","Record not found"));}
 @ExceptionHandler(IllegalArgumentException.class)ResponseEntity<Map<String,String>> invalidState(IllegalArgumentException ex){return ResponseEntity.badRequest().body(Map.of("error","Invalid request"));}
}
