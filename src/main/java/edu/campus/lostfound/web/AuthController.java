package edu.campus.lostfound.web;
import edu.campus.lostfound.domain.*;import edu.campus.lostfound.repository.UserRepository;import jakarta.validation.Valid;import jakarta.validation.constraints.*;import org.springframework.security.crypto.password.PasswordEncoder;import org.springframework.stereotype.Controller;import org.springframework.ui.Model;import org.springframework.validation.BindingResult;import org.springframework.web.bind.annotation.*;import org.springframework.web.servlet.mvc.support.RedirectAttributes;
@Controller public class AuthController{
 private final UserRepository users;private final PasswordEncoder encoder;public AuthController(UserRepository users,PasswordEncoder encoder){this.users=users;this.encoder=encoder;}
 @GetMapping("/login")String login(){return "login";}
 @GetMapping("/register")String register(Model model){model.addAttribute("form",new RegisterForm("","",""));return "register";}
 @PostMapping("/register")String create(@Valid @ModelAttribute("form")RegisterForm form,BindingResult errors,Model model,RedirectAttributes flash){if(users.findByEmailIgnoreCase(form.email()).isPresent())errors.rejectValue("email","duplicate","An account already uses this email.");if(errors.hasErrors())return "register";users.save(new AppUser(form.name().trim(),form.email().trim().toLowerCase(),encoder.encode(form.password()),Role.USER));flash.addFlashAttribute("notice","Account created. Sign in to continue.");return "redirect:/login";}
 public record RegisterForm(@NotBlank @Size(max=100)String name,@NotBlank @Email @Size(max=190)String email,@NotBlank @Size(min=10,max=72)String password){}
}
