package edu.campus.lostfound.config;
import edu.campus.lostfound.domain.*;import edu.campus.lostfound.repository.UserRepository;import org.springframework.beans.factory.annotation.Value;import org.springframework.boot.CommandLineRunner;import org.springframework.context.annotation.Bean;import org.springframework.context.annotation.Configuration;import org.springframework.security.crypto.password.PasswordEncoder;
@Configuration public class BootstrapConfig{
 @Bean CommandLineRunner ensureAdmin(UserRepository users,PasswordEncoder encoder,@Value("${app.security.initial-admin-email}")String email,@Value("${app.security.initial-admin-password}")String password){return args->{if(users.findByEmailIgnoreCase(email).isEmpty())users.save(new AppUser("Campus Administrator",email,encoder.encode(password),Role.ADMIN));};}
}
