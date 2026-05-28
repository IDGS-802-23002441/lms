using ApiSensores.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiSensores.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<Lectura> Lecturas => Set<Lectura>();
    }
}