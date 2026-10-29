package edu.campus.lostfound.repository;
import edu.campus.lostfound.domain.AppUser;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
public interface UserRepository extends JpaRepository<AppUser,Long>{ Optional<AppUser> findByEmailIgnoreCase(String email); }
